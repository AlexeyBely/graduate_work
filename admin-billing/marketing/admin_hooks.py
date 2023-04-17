from django.contrib import admin

from marketing.models import Tariff
from marketing.grpc_auth_service.roles_control_client import (create_new_role, 
                                                              update_role)


class HookTariffAdmin(admin.ModelAdmin):

    def save_model(self, request, obj: Tariff, form, change):
        """Create or update the role in auth service."""
        if obj.auth_role_id is None:
            role_id = create_new_role(name=obj.role)
            obj.auth_role_id = role_id
            obj.save()
        else:
            result = update_role(role_id=obj.auth_role_id, name=obj.role)
            if result is True:
                obj.save()
