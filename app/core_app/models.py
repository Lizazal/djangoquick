from django.db import models
from django.conf import settings


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
