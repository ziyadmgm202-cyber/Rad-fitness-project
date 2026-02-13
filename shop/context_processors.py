from cart.models import Cart

def cartcount(request):
    count=0
    if request.user.is_authenticated:
        u=request.user
        try:
            c=Cart.objects.filter(user=u)
            for i in c:
                count=count+i.quantity
        except:
            pass
    return {'count': count}


from random import sample
from .models import Product


def random_category_products(request):

    # Get only products that are in stock
    all_products = list(Product.objects.filter(stock__gt=0))

    # Pick 6 random products
    random_products = sample(all_products, min(len(all_products), 6))

    return {
        'random_products': random_products
    }
