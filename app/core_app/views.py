from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Company, Storage, Supplier, Product, Supply
from .permissions import CompanyPermission, StoragePermission, CompanyMemberPermission, ProductPermission, IsCompanyOwnerPermission
from .serializers import CompanySerializer, StorageSerializer, SupplierSerializer, ProductSerializer, SupplySerializer, AttachEmployeeSerializer


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
            raise PermissionDenied('Только владелец компании может добавить склад.')
        serializer.save(company=user.owned_company)


class StorageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [StoragePermission]


class SupplierListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        if self.request.user.company is None:
            raise PermissionDenied('Пользователь не привязан к компании.')
        serializer.save()


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [CompanyMemberPermission]


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(storage__company=self.request.user.company)

    def perform_create(self, serializer):
        if self.request.user.company is None:
            raise PermissionDenied('Пользователь не привязан к компании.')
        serializer.save()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]


class SupplyListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Supply.objects.filter(supplier__company=self.request.user.company)

    def perform_create(self, serializer):
        if self.request.user.company is None:
            raise PermissionDenied('Пользователь не привязан к компании.')
        serializer.save()


class AttachEmployeeView(generics.GenericAPIView):
    serializer_class = AttachEmployeeSerializer
    permission_classes = [IsCompanyOwnerPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'company': user.company_id,
            },
            status=status.HTTP_200_OK,
        )
