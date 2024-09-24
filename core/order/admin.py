from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid', 'updated_time')
    list_filter = ('is_paid', 'user')
    inlines = (OrderItemInline,)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active')


admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
