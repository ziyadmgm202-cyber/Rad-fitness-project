from django.urls import path
from .views import AddItemsView



urlpatterns = [
    path('add-items/', AddItemsView.as_view(), name='add_items'),
]
