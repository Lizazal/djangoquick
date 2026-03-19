from rest_framework import serializers
from .models import Company, Storage


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
