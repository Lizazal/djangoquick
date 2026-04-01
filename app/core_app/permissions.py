from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class CompanyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and obj.owner == request.user


class StoragePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return user.company_id == obj.company_id
        return hasattr(user, 'owned_company') and obj.company_id == user.owned_company.id


class CompanyMemberPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.company_id == obj.company_id


class ProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.company_id == obj.storage.company_id


class IsCompanyOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_company_owner
