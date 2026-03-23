from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'username', 'is_company_owner', 'company', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'username')

    fieldsets = BaseUserAdmin.fieldsets + (('Информация о компании', {'fields': ('is_company_owner', 'company')}),)

    add_fieldsets = BaseUserAdmin.add_fieldsets + (('Информация о компании', {'fields': ('email', 'username', 'is_company_owner', 'company')}),)
