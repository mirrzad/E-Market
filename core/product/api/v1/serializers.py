from rest_framework import serializers
from product.models import Product, Category


class ProductIdTitleRelationalField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.id} - {value.title}'


class ProductSerializer(serializers.ModelSerializer):
    category = ProductIdTitleRelationalField(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
