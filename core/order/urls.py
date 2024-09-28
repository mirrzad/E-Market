from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('list/', views.OrderListView.as_view(), name='order-list'),
    path('details/<int:order_id>/', views.OrderDetailsView.as_view(), name='order-details'),
    path('coupon/<int:order_id>/', views.CouponApplyView.as_view(), name='apply-coupon'),

    path('cart/', views.CartView.as_view(), name='cart-page'),
    path('cart/add/<int:variant_id>/', views.AddCartView.as_view(), name='add-cart'),
    path('cart/remove/<int:product_id>/', views.RemoveCartView.as_view(), name='remove-cart'),
]
