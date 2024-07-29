from django.shortcuts import render
from django.views import View
from product.models import Product, Category


class HomeView(View):
    template_name = 'home/home-page.html'

    def get(self, request, category_slug=None):
        products = Product.objects.filter(is_available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            products = products.filter(category=category)
        return render(request, self.template_name, {'products': products, 'categories': categories})
