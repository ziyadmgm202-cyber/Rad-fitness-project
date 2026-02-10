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