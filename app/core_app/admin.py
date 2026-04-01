from django.contrib import admin
from .models import Company, Storage, Supplier, Product, Supply, SupplyProduct


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'inn', 'owner', 'created_at')
    search_fields = ('title', 'inn', 'owner__email')


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'address')
    search_fields = ('company__title', 'address')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'inn', 'company')
    search_fields = ('title', 'inn', 'company__title')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'quantity', 'purchase_price', 'sale_price', 'storage')
    search_fields = ('title',)


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'delivery_date')
    search_fields = ('supplier__title',)


@admin.register(SupplyProduct)
class SupplyProductAdmin(admin.ModelAdmin):
    list_display = ('supply', 'product', 'quantity')
