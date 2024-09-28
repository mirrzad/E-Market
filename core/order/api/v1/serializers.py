from rest_framework import serializers
from order.models import Order, OrderItem, Coupon


class OrderIdTitleRelationField(serializers.RelatedField):
    def to_representation(self, value):
        return f'id: {value.id} | username: {value.phone_number}'


class OrderSerializer(serializers.ModelSerializer):
    user = OrderIdTitleRelationField(read_only=True)
    total_payment = serializers.IntegerField()

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemIdTitleRelationField(serializers.RelatedField):
    def to_representation(self, value):
        return f'id: {value.product.id} | title: {value.product.title} ' \
               f'| variant_id: {value.id} | attributes: {value.attributes}'


class OrderItemsSerializer(serializers.ModelSerializer):
    product = OrderItemIdTitleRelationField(read_only=True)
    get_payment_amount = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = '__all__'
