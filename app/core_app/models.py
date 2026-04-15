from django.db import models
from django.conf import settings
from django.utils import timezone


class Company(models.Model):
    title = models.CharField('Название', max_length=255)
    inn = models.CharField('ИНН', max_length=20, unique=True)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_company',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.title


class Storage(models.Model):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name='storage',
        verbose_name='Компания'
    )
    address = models.CharField('Адрес склада', max_length=255)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.company.title} — {self.address}'


class Supplier(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='suppliers',
        verbose_name='Компания'
    )
    title = models.CharField('Название', max_length=255)
    inn = models.CharField('ИНН', max_length=20)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField('Название', max_length=255)
    purchase_price = models.DecimalField('Закупочная цена', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Цена продажи', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Количество', default=0)
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Склад'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Supply(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='supplies',
        verbose_name='Поставщик'
    )
    delivery_date = models.DateTimeField('Дата поставки', auto_now_add=True)
    products = models.ManyToManyField(
        Product,
        through='SupplyProduct',
        related_name='supplies'
    )

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

    def __str__(self):
        return f'Поставка №{self.id} от {self.supplier.title}'


class SupplyProduct(models.Model):
    supply = models.ForeignKey(
        Supply,
        on_delete=models.CASCADE,
        related_name='supply_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='supply_products'
    )
    quantity = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'Товар в поставке'
        verbose_name_plural = 'Товары в поставке'

    def __str__(self):
        return f'{self.product.title} — {self.quantity}'


class Sale(models.Model):
    buyer_name = models.CharField('Имя покупателя', max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Компания'
    )
    sale_date = models.DateTimeField('Дата продажи', default=timezone.now)
    products = models.ManyToManyField(
        Product,
        through='ProductSale',
        related_name='sales'
    )

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

    def __str__(self):
        return f'Продажа №{self.id} — {self.buyer_name}'


class ProductSale(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_sales',
        verbose_name='Товар'
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='product_sales',
        verbose_name='Продажа'
    )
    quantity = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'Товар в продаже'
        verbose_name_plural = 'Товары в продаже'

    def __str__(self):
        return f'{self.product.title} — {self.quantity}'
