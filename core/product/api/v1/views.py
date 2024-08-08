from rest_framework.views import APIView
from product.models import Product
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.core.paginator import Paginator


class ProductListApiView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        page_num = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 2)
        paginator = Paginator(products, limit)
        try:
            ser_data = self.serializer_class(instance=paginator.page(page_num), many=True)
        except:
            return Response({'detail': 'This page contains no results'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)


class ProductUpdateView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        srz_data = self.serializer_class(instance=product, data=request.data, partial=True)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)


class ProductDeleteView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'detail': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
