from rest_framework import serializers
from .models import Company, Storage, Supplier, Product, Supply, SupplyProduct
from django.contrib.auth import get_user_model

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Company
        fields = ('id', 'title', 'inn', 'owner', 'created_at')
        read_only_fields = ('id', 'owner', 'created_at')

    def validate(self, attrs):
        user = self.context['request'].user
        request_method = self.context['request'].method
        if request_method == 'POST':
            if user.company_id is not None:
                raise serializers.ValidationError("Пользователь уже является частью другой компании.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        company = Company.objects.create(owner=user, **validated_data)
        user.is_company_owner = True
        user.company = company
        user.save(update_fields=['is_company_owner', 'company'])
        return company


class StorageSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source='company.id')

    class Meta:
        model = Storage
        fields = ('id', 'company', 'address')
        read_only_fields = ('id', 'company')

    def validate(self, attrs):
        user = self.context['request'].user
        request_method = self.context['request'].method
        if request_method == 'POST':
            if not hasattr(user, 'owned_company'):
                raise serializers.ValidationError("Только владелец компании может создать склад.")
            if getattr(user.owned_company, 'storage', None) is not None:
                raise serializers.ValidationError("У компании уже есть склад.")
        return attrs

    def create(self, validated_data):
        return Storage.objects.create(**validated_data)


class SupplierSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source='company.id')

    class Meta:
        model = Supplier
        fields = ('id', 'title', 'inn', 'company')
        read_only_fields = ('id', 'company')

    def create(self, validated_data):
        return Supplier.objects.create(company=self.context['request'].user.company, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    quantity = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'purchase_price', 'sale_price', 'quantity', 'storage')
        read_only_fields = ('id', 'quantity')

    def validate_storage(self, value):
        user = self.context['request'].user
        if user.company_id != value.company_id:
            raise serializers.ValidationError('Нельзя работать со складом чужой компании.')
        return value

    def create(self, validated_data):
        return Product.objects.create(quantity=0, **validated_data)


class SupplyProductInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class SupplySerializer(serializers.ModelSerializer):
    supplier_id = serializers.IntegerField(write_only=True)
    products = SupplyProductInputSerializer(many=True, write_only=True)

    class Meta:
        model = Supply
        fields = ('id', 'supplier_id', 'products', 'delivery_date')
        read_only_fields = ('id', 'delivery_date')

    def validate(self, attrs):
        user = self.context['request'].user
        supplier_id = attrs.get('supplier_id')
        products_data = attrs.get('products', [])

        if not products_data:
            raise serializers.ValidationError('Поставка должна содержать хотя бы один товар.')

        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            raise serializers.ValidationError('Поставщик не найден.')

        if supplier.company_id != user.company_id:
            raise serializers.ValidationError('Поставщик не относится к компании пользователя.')

        for item in products_data:
            try:
                product = Product.objects.get(id=item['id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Товар с id={item['id']} не найден.")

            if product.storage.company_id != user.company_id:
                raise serializers.ValidationError(
                    f"Товар '{product.title}' не принадлежит компании пользователя."
                )

        attrs['supplier'] = supplier
        return attrs

    def create(self, validated_data):
        supplier = validated_data.pop('supplier')
        products_data = validated_data.pop('products')

        supply = Supply.objects.create(supplier=supplier)

        for item in products_data:
            product = Product.objects.get(id=item['id'])
            quantity = item['quantity']

            SupplyProduct.objects.create(
                supply=supply,
                product=product,
                quantity=quantity
            )

            product.quantity += quantity
            product.save(update_fields=['quantity'])

        return supply


class AttachEmployeeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs['email']
        request_user = self.context['request'].user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь с таким email не найден.')
        if user == request_user:
            raise serializers.ValidationError('Нельзя прикрепить самого себя.')
        if user.is_company_owner:
            raise serializers.ValidationError('Нельзя прикрепить владельца компании.')
        if user.company_id is not None:
            raise serializers.ValidationError('Пользователь уже прикреплён к компании.')
        attrs['user_obj'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user_obj']
        user.company = self.context['request'].user.company
        user.save(update_fields=['company'])
        return user
