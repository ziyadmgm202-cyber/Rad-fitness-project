from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from cart.models import Cart,Order,Order_items
from cart.forms import OrderForm
import razorpay
import uuid
from django.conf import settings



# Create your views here.
@method_decorator(login_required,name="dispatch")
class AddToCartView(View):
    def get(self, request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c = Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('cartview')
    
@method_decorator(login_required,name="dispatch")
class CartView(View):
    def get(self, request):
        u=request.user
        c=Cart.objects.filter(user=u)
        sum=0
        for i in c:
            sum = sum + i.subtotal()
        print(c)
        context = {'cart':c,'total':sum}
        return render(request, 'cart.html',context)
    
@method_decorator(login_required,name="dispatch")
class DecrementCartView(View):
    def get(self, request,i):
        c = Cart.objects.get(id=i)
        if(c.quantity>1):
            c.quantity -= 1
            c.save()
        else:
            c.delete()
        return redirect('cartview')


@method_decorator(login_required,name="dispatch")
class Increment_cart(View):
    def get(self,request,i):
        p=Cart.objects.get(id=i)
        p.quantity+=1
        p.save()
        return redirect('cartview')


@method_decorator(login_required,name="dispatch")
class DeleteProduct(View):
    def get(self, request,i):
        c=Cart.objects.get(id=i)
        c.delete()
        return redirect('cart:cartview')

import uuid
import razorpay
from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, Order, Order_items
from .forms import OrderForm
from django.db import transaction




@method_decorator(login_required,name="dispatch")
class CheckoutView(View):
    def get(self, request):
        u = request.user
        cart_items = Cart.objects.filter(user=u)
        
        # Calculate total to show on checkout page
        total = sum(i.subtotal() for i in cart_items)
        
        form = OrderForm()
        context = {
            'form': form,
            'cart_items': cart_items,
            'total': total
        }
        return render(request, 'checkout.html', context)

    def post(self, request):
        form = OrderForm(request.POST)
        u = request.user
        cart_items = Cart.objects.filter(user=u)
        
        if form.is_valid():
            # 1. Calculate Total Amount
            total_amount = sum(i.subtotal() for i in cart_items)
            
            # 2. Create Order Instance (Unconfirmed)
            o = form.save(commit=False)
            o.user = u
            o.amount = total_amount
            o.save()

            if o.payment_method == 'online':

                client = razorpay.Client(
                    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
                )

                data = {
                    'amount': int(total_amount * 100),
                    'currency': 'INR',
                    'receipt': f"receipt_{o.id}"
                }

                response_payment = client.order.create(data)

                o.order_id = response_payment['id']
                o.save()

                context = {
                    'payment': response_payment,
                    'total': total_amount,
                    'order': o,
                    'razorpay_key': settings.RAZORPAY_KEY_ID   # 🔥 ADD THIS LINE
                }

                return render(request, 'payment_gateway.html', context)

            
            else:
                # --- COD FLOW ---
                with transaction.atomic():
                    # Generate a custom COD ID
                    o.order_id = 'ORD_COD' + uuid.uuid4().hex[:14].upper()
                    o.is_ordered = True
                    o.save()

                    # Transfer items and update stock
                    for i in cart_items:
                        Order_items.objects.create(
                            order=o, 
                            product=i.product, 
                            quantity=i.quantity
                        )
                        # Update Inventory
                        i.product.stock -= i.quantity
                        i.product.save()

                    # Clear Cart
                    cart_items.delete()
                    
                return render(request, 'order_success.html', {'order': o})

        return redirect('checkout')
#csrf excempt-to ignore csrf verification:

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from cart.models import Order, Cart, Order_items
from django.conf import settings


@method_decorator(login_required,name="dispatch")
@method_decorator(csrf_exempt, name='dispatch')
class Paymentsuccess(View):

    def get(self, request):

        print("GET DATA:", request.GET)   # Debug

        razorpay_order_id = request.GET.get('order_id')
        razorpay_payment_id = request.GET.get('payment_id')
        razorpay_signature = request.GET.get('signature')

        try:
            o = Order.objects.get(order_id=razorpay_order_id)
        except Order.DoesNotExist:
            return render(request, 'error.html', {'message': 'Order Not Found'})

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': o.order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            print("Signature Error:", e)
            return render(request, 'error.html', {'message': 'Payment verification failed'})

        with transaction.atomic():
            o.is_ordered = True
            o.save()

            u = o.user
            cart_items = Cart.objects.filter(user=u)

            for i in cart_items:
                Order_items.objects.create(
                    order=o,
                    product=i.product,
                    quantity=i.quantity
                )
                i.product.stock -= i.quantity
                i.product.save()

            cart_items.delete()

        return render(request, 'payment_success.html', {
            'order': o,
            'payment_id': razorpay_payment_id,
            'razorpay_key': settings.RAZORPAY_KEY_ID 
        })

@method_decorator(login_required,name="dispatch")
class OrderDetailView(View):
    def get(self, request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context = {'orders':o}
        return render(request, 'order_detail.html', context)


# Create your views here.
