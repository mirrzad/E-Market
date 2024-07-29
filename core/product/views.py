from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product
from order.forms import CartAddForm


class ProductDetailView(View):
    template_name = 'product/product-details.html'
    form_class = CartAddForm

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, self.template_name, {'product': product, 'form': self.form_class})
