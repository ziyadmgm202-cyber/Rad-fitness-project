from django.contrib import admin
from django.urls import path

from search.views import SearchView

app_name = 'search'
urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
]