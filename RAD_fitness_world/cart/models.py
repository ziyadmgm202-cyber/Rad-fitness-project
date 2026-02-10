from django.contrib.auth.models import User
from django.db import models
from shop.models import Product


# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    def subtotal(self):
        return self.quantity * self.product.price

class Order(models.Model):
    order_id=models.CharField(max_length=100,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()
    address=models.TextField(max_length=100)
    phone=models.IntegerField()
    payment_method=models.CharField(max_length=100)
    ordered_date=models.DateTimeField(auto_now_add=True)
    is_ordered=models.BooleanField(default=False)
    delivery_status=models.CharField(default="Pending",max_length=100)

    def __str__(self):
        return self.order_id

class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='products')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.order.order_id
