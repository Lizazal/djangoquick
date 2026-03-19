from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Company, Storage
from .serializers import CompanySerializer, StorageSerializer
from .permissions import CompanyPermission, StoragePermission


class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [CompanyPermission]


class StorageCreateView(generics.CreateAPIView):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'owned_company'):
            raise PermissionDenied("Только владелец компании может добавить склад.")
        serializer.save(company=user.owned_company)


class StorageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [StoragePermission]
