from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Tariff, PersonalDiscount, MonthsDiscount, Promocode


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = (
        'role',
        'price',
    )


@admin.register(PersonalDiscount)
class PersonalDiscountAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'discount',
    )


@admin.register(MonthsDiscount)
class MonthsDiscountAdmin(admin.ModelAdmin):
    list_display = (
        'amount_months',
        'discount',
    )


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'expiration',
    )