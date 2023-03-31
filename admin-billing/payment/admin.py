from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Customer, PrivilegedRole, Payment


class PrivilegedRoleInline(admin.TabularInline):
    model = PrivilegedRole
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'email',
    )
    inlines = (
        PrivilegedRoleInline,
        PaymentInline,
    )
    search_fields = (
        'email',
    )
