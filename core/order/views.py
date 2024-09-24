from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from product.models import ProductVariant
from .models import OrderItem, Order, Coupon
from .cart import Cart
from .forms import CartAddForm, CouponApplyForm
from django.utils import timezone
from django.contrib import messages


class CartView(View):
    template_name = 'order/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


class AddCartView(View):
    form_class = CartAddForm

    def post(self, request, variant_id):
        cart = Cart(request)
        variant = get_object_or_404(ProductVariant, id=variant_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(variant, cd['quantity'])
        return redirect(variant.product.get_absolute_url())


class RemoveCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return redirect('order:cart-page')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product_name'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        return redirect('order:order-details', order.id)


class OrderDetailsView(LoginRequiredMixin, View):
    template_name = 'order/order-details.html'
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {'order': order, 'form': self.form_class})


class OrderListView(LoginRequiredMixin, View):
    template_name = 'order/order-list.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-id')
        return render(request, self.template_name, {'orders': orders})


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = timezone.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(
                    code__exact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    is_active=True
                )
            except Coupon.DoesNotExist:
                messages.error(request, 'Code is not valid.', 'danger')
                return redirect('order:order-details', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            coupon.is_active = False
            coupon.save()
            messages.success(request, 'Code applied successfully.', 'success')
        return redirect('order:order-details', order_id)
