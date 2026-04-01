from django.urls import path
from .views import (CompanyCreateView, CompanyDetailView, StorageCreateView, StorageDetailView,
                    SupplierListCreateView, SupplierDetailView, ProductListCreateView,
                    ProductDetailView, SupplyListCreateView, AttachEmployeeView,)

urlpatterns = [
    path('companies/create/', CompanyCreateView.as_view(), name='company-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('storages/create/', StorageCreateView.as_view(), name='storage-create'),
    path('storages/<int:pk>/', StorageDetailView.as_view(), name='storage-detail'),
    path('suppliers/', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('supplies/', SupplyListCreateView.as_view(), name='supply-list-create'),
    path('companies/attach/', AttachEmployeeView.as_view(), name='attach-employee'),
]
