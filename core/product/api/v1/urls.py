from django.urls import path
from . import views

app_name = 'product_api'

urlpatterns = [
    path('list/', views.ProductListApiView.as_view(), name='product-list-api'),
    path('details/<int:pk>/', views.ProductDetailsApiView.as_view(), name='product-details-api'),
    path('create/', views.ProductCreateView.as_view(), name='product-create-api'),
    path('variant/create/', views.ProductVariantCreateView.as_view(), name='product-variant-create-api'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update-api'),
    path('variant/update/<int:pk>/', views.ProductVariantUpdateView.as_view(), name='product-variant-update-api'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete-api'),
    path('variant/delete/<int:pk>/', views.ProductVariantDeleteView.as_view(), name='product-variant-delete-api'),
]
