from django.urls import path
from . import views

app_name = 'order_api'

urlpatterns = [
    path('list/', views.OrderListApiView.as_view(), name='order_list_api'),
    path('create/', views.OrderCreateApiView.as_view(), name='order_create_api'),
    path('details/<int:order_id>/', views.OrderDetailsApiView.as_view(), name='order_details_api'),

    path('coupon/<int:order_id>/', views.CouponApplyApiView.as_view(), name='apply_coupon_api'),
    path('coupon/create/', views.CouponCreateApiView.as_view(), name='create_coupon_api'),
    path('coupon/list/', views.CouponListApiView.as_view(), name='list_coupon_api'),

    path('cart/', views.CartApiView.as_view(), name='cart_api'),
    path('cart/add/<int:variant_id>/', views.CartAddApiView.as_view(), name='cart_add_api'),
    path('cart/delete/<int:variant_id>/', views.CartDeleteApiView.as_view(), name='cart_delete_api'),
]
