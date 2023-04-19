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
        'get_privileged_roles',
    )
    inlines = (
        PrivilegedRoleInline,
        PaymentInline,
    )
    search_fields = (
        'email',
    )

    def get_privileged_roles(self, obj):
        roles = obj.privilegedrole_set.all()
        return [f'{role.role_payment} up to {role.end_payment:%d-%m-%Y %H:%M}' 
                for role in roles]
    
    get_privileged_roles.short_description = _('Role')


admin.site.site_header = 'Администрирование оплаты' 
admin.site.index_title = 'Администрирование оплаты'               
admin.site.site_title = 'Администрирование оплаты' 

     
