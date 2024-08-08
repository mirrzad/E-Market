from django.urls import path
from . import views

app_name = 'product_api'

urlpatterns = [
    path('list/', views.ProductListApiView.as_view(), name='product-list-api'),
    path('create/', views.ProductCreateView.as_view(), name='product-create-api'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update-api'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete-api'),
]
