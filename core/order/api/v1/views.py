from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from permissions import IsOwner
from rest_framework.response import Response
from rest_framework import status
from order.cart import Cart
from .serializers import OrderSerializer, OrderItemsSerializer, CouponSerializer
from order.models import Order, OrderItem, Coupon
from product.models import ProductVariant
from django.shortcuts import get_object_or_404
from django.utils import timezone


class OrderListApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        srz_data = self.serializer_class(instance=orders, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class OrderDetailsApiView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = OrderItemsSerializer

    def get(self, request, order_id):
        order_items = OrderItem.objects.filter(order__id=order_id)
        self.check_object_permissions(request, order_items.first())
        srz_data = self.serializer_class(instance=order_items, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class OrderCreateApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemsSerializer

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
        return Response({'details': f'order: {order.id} created.'}, status=status.HTTP_201_CREATED)


class CartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        return Response({'cart': cart.cart, 'total_price': cart.get_total_price()}, status=status.HTTP_200_OK)


class CartAddApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, variant_id):
        cart = Cart(request)
        variant = get_object_or_404(ProductVariant, id=variant_id)
        quantity = request.data.get('quantity', 1)
        cart.add(variant, int(quantity))
        return Response({'details': 'Item added to cart.'}, status=status.HTTP_201_CREATED)


class CartDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, variant_id):
        cart = Cart(request)
        cart.remove(variant_id)
        return Response({'details': f'product with variant id: {variant_id} deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)


class CouponCreateApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CouponSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)


class CouponListApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CouponSerializer

    def get(self, request):
        coupons = Coupon.objects.filter(is_active=True)
        srz_data = self.serializer_class(instance=coupons, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class CouponApplyApiView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CouponSerializer

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        self.check_object_permissions(request, order.items.first())
        code = request.data.get('code', None)
        if code:
            now = timezone.now()
            try:
                coupon = Coupon.objects.get(
                    code__exact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    is_active=True
                )
            except Coupon.DoesNotExist:
                return Response({'details': 'Code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

            order.discount = coupon.discount
            order.save()
            coupon.is_active = False
            coupon.save()
            return Response({'details': 'Code applied successfully.'}, status=status.HTTP_200_OK)
        return Response({'details': 'Code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)
