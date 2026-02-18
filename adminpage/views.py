from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth.models import User
from cart.models import Order
from .forms import CategoryForm, ProductForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from shop.models import Product




def admin_required(fun):
    def wrapper(request):
        if not request.user.is_superuser:
            return HttpResponse('not allowed')
        else:
            return fun(request)
    return wrapper



@method_decorator(admin_required,name="dispatch")
@method_decorator(login_required,name="dispatch")
class AddItemsView(View):

    template_name = "admin/add_items.html"

    # -------------------------------
    # 🔹 Dashboard Stats
    # -------------------------------
    def get_dashboard_stats(self):
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(delivery_status="Pending").count()
        completed_orders = Order.objects.filter(delivery_status="Delivered").count()
        cancelled_orders = Order.objects.filter(delivery_status="Cancelled").count()

        total_revenue = Order.objects.filter(
            is_ordered=True
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        total_users = User.objects.count()
        latest_order = Order.objects.order_by("-ordered_date").first()

        return {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
            "total_revenue": total_revenue,
            "total_users": total_users,
            "latest_order": latest_order,
        }

    # -------------------------------
    # 🔹 GET
    # -------------------------------
    def get(self, request):

        category_form = CategoryForm(prefix="cat")

        edit_id = request.GET.get("edit")
        delete_id = request.GET.get("delete")

        # 🔥 DELETE PRODUCT
        if delete_id:
            Product.objects.filter(id=delete_id).delete()
            messages.success(request, "Product deleted successfully 🗑️")
            return redirect("add_items")

        # 🔥 EDIT PRODUCT
        if edit_id:
            product = Product.objects.get(id=edit_id)
            product_form = ProductForm(instance=product, prefix="pro")
        else:
            product_form = ProductForm(prefix="pro")

        # All products list
        products = Product.objects.all().order_by("-id")

        # Orders pagination (your existing)
        orders = Order.objects.all().order_by("-ordered_date")
        paginator = Paginator(orders, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "category_form": category_form,
            "product_form": product_form,
            "products": products,
            "edit_id": edit_id,
            "page_obj": page_obj,
        }

        context.update(self.get_dashboard_stats())

        return render(request, self.template_name, context)

    # -------------------------------
    # 🔹 POST
    # -------------------------------
    def post(self, request):

        category_form = CategoryForm(prefix="cat")

        edit_id = request.POST.get("edit_id")

        # 🔥 ADD / UPDATE PRODUCT
        if "pro_submit" in request.POST:

            if edit_id:
                product = Product.objects.get(id=edit_id)
                product_form = ProductForm(
                    request.POST,
                    request.FILES,
                    instance=product,
                    prefix="pro"
                )
            else:
                product_form = ProductForm(
                    request.POST,
                    request.FILES,
                    prefix="pro"
                )

            if product_form.is_valid():
                product_form.save()

                if edit_id:
                    messages.success(request, "Product updated successfully ✏️")
                else:
                    messages.success(request, "Product added successfully ✅")

                return redirect("add_items")

        # 🔥 ADD CATEGORY
        elif "cat_submit" in request.POST:
            category_form = CategoryForm(request.POST, request.FILES, prefix="cat")
            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Category added successfully ✅")
                return redirect("add_items")

        return redirect("add_items")
