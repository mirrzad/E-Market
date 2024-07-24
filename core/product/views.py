from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product


class ProductDetailView(View):
    template_name = 'product/product-details.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, self.template_name, {'product': product})
