from django.urls import path
from . import views

app_name = 'product_api'

urlpatterns = [
    path('list/', views.ProductListApiView.as_view(), name='product_list_api'),
    path('details/<int:pk>/', views.ProductDetailsApiView.as_view(), name='product_details_api'),
    path('create/', views.ProductCreateView.as_view(), name='product_create_api'),
    path('variant/create/', views.ProductVariantCreateView.as_view(), name='product_variant_create_api'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update_api'),
    path('variant/update/<int:pk>/', views.ProductVariantUpdateView.as_view(), name='product_variant_update_api'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete_api'),
    path('variant/delete/<int:pk>/', views.ProductVariantDeleteView.as_view(), name='product_variant_delete_api'),

    path('category/create/', views.CategoryCreateApiView.as_view(), name='category_create_api'),
    path('category/details/<int:pk>/', views.CategoryDetailsApiView.as_view(), name='category_details_api'),
    path('category/list/', views.CategoryListApiView.as_view(), name='category_list_api'),
]
