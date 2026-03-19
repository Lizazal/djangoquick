from django.contrib import admin
from .models import Company, Storage


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'inn', 'owner', 'created_at')
    search_fields = ('title', 'inn', 'owner__email')


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'address')
    search_fields = ('company__title', 'address')
