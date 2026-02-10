from django.shortcuts import render
from django.db.models import Q
from django.views import View
from shop.models import Product
# Create your views here.
class SearchView(View):
    def get(self, request):
        query = request.GET['q']  # Reads the keyword
        print(query)
        # ORM query to filter records from the table
        b = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(
            stock__icontains=query))  # __icontains-lookups
        print(b)
        context = {'p': b,'query': query}
        return render(request, 'search.html',context)