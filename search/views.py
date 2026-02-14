from django.shortcuts import render
from django.db.models import Q
from django.views import View
from shop.models import Product


class SearchView(View):
    def get(self, request):

        query = request.GET.get('q')

        products = Product.objects.all()

        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(stock__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()

        context = {
            'result': products,
            'query': query
        }

        return render(request, 'search.html', context)
