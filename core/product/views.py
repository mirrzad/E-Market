from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, ProductVariant
from order.forms import CartAddForm


class ProductDetailView(View):
    template_name = 'product/product-details.html'
    form_class = CartAddForm

    def get(self, request, slug):
        variants = ProductVariant.objects.filter(product__slug=slug)
        return render(request, self.template_name,
                      {'variants': variants, 'form': self.form_class})
