from django.shortcuts import render
from django.views import View
from product.models import Product


class HomeView(View):
    template_name = 'home/home-page.html'

    def get(self, request):
        products = Product.objects.filter(is_available=True)
        return render(request, self.template_name, {'products': products})
