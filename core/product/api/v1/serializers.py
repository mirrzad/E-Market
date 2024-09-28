from rest_framework import serializers
from product.models import Product, Category, ProductVariant


class ProductIdTitleRelationalField(serializers.RelatedField):
    def to_representation(self, value):
        return f'id: {value.id} | title: {value.title}'


class ProductVariantsRelationalField(serializers.RelatedField):
    def to_representation(self, value):
        return f'id: {value.id} | price: {value.price} | attributes: {value.attributes}'


class ProductSerializer(serializers.ModelSerializer):
    category = ProductIdTitleRelationalField(read_only=True)
    variants = ProductVariantsRelationalField(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = '__all__'


class CategoryIdTitleRelationalField(serializers.RelatedField):
    def to_representation(self, value):
        return f'id: {value.id} | title: {value.title}'


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = CategoryIdTitleRelationalField(read_only=True, many=True)

    class Meta:
        model = Category
        fields = '__all__'
