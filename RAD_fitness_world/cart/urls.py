from django.contrib import admin
from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cartview'),
    path('addcart/<int:i>', views.AddCartView.as_view(), name='addcart'),
    path('removecart/<int:i>', views.DecrementCartView.as_view(), name='minuscart'),
    path('deleteproduct/<int:i>', views.DeleteProduct.as_view(), name='dltpdt'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('paymentsuccess/', views.Paymentsuccess.as_view(), name='paymentsuccess'),
    path('orderdetail/', views.OrderDetailView.as_view(), name='orderdetail'),
]