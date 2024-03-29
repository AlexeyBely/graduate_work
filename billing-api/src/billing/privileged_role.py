import uuid
from datetime import datetime, timedelta

from core.config import settings
from crud_service.crud_billing_abc import BaseCrudBilling
from crud_service.read_marketing_abc import BaseReadMarketing
from grpc_service.auth_service import roles_control_client as rc_client
from grpc_service.notify_service import message_sender_client as ms_client
from grpc_service.notify_service.message_sender_client import SubscribeMessage
from schemas.billing_schemas import (PaymentSchema, PrivilegedRoleBase,
                                     PrivilegedRoleSchema, SubStatusEnum)


class SubscribePrivilegedRoles:
    """Subscription (subscription renewal) for privileged roles."""

    def __init__(self, read_marketing: BaseReadMarketing, crud_billing: BaseCrudBilling):
        self.read_marketing = read_marketing
        self.crud_billing = crud_billing

    async def subscribe_paid_role(self, payment: PaymentSchema) -> bool:
        """Subscribe to Paid Preferred Role.
        
        Return True at successful subscribe and passed to auth service. 
        """
        role = await self._get_payment_role(payment)
        if role is None:
            role = await self.crud_billing.create_privileged_role(
                PrivilegedRoleBase(
                    customer_id=payment.customer_id,
                    status=SubStatusEnum.SUBSCRIBE,
                    role_payment=payment.role_payment,
                    end_payment=self._payment_months(True, payment, datetime.now()) 
                )
            )
        else:
            if role.status == SubStatusEnum.SUBSCRIBE:            
                role.end_payment = self._payment_months(True, payment, role.end_payment) 
            else: 
                role.status = SubStatusEnum.SUBSCRIBE   
                role.end_payment = self._payment_months(True, payment, datetime.now()) 
            await self.crud_billing.update_privileged_role(
                privel_role_id=role.id,
                privel_role=PrivilegedRoleBase(**role.__dict__)
            )
        return await self._provided_revoked_role(True, payment, role)

    async def unsubscribe_paid_role(self, payment: PaymentSchema) -> bool:
        """Unsubscribe to Paid Preferred Role.
        
        Return True at successful unsubscribe and passed to auth service. 
        """
        role = await self._get_payment_role(payment)
        if role is None:
            return False
        role.end_payment = self._payment_months(False, payment, role.end_payment)
        if role.end_payment < datetime.now():
            role.status = SubStatusEnum.EXPIRED
            result = await self._provided_revoked_role(False, payment, role)
            if result is False:
                return False
        await self.crud_billing.update_privileged_role(
            privel_role_id=role.id,
            privel_role=PrivilegedRoleBase(**role.__dict__)
        )
        return True
    
    async def check_end_subscribe(self) -> None:
        """Check subscription expiration."""        
        roles = await self.crud_billing.get_privileged_roles(   
            filter_status=SubStatusEnum.SUBSCRIBE,
            time_after=timedelta(days=settings.payment_days_expired)
        )
        for role in roles:            
            user_id, tariff = await self._get_user_and_tariff(role)
            result = await rc_client.grpc_auth_revoke_role(
                user_id=user_id,
                role_id=tariff.auth_role_id,
                jti=str(uuid.uuid4())
            )
            if result is True:
                role.status = SubStatusEnum.EXPIRED
                await self.crud_billing.update_privileged_role(
                    privel_role_id=role.id,
                    privel_role=PrivilegedRoleBase(**role.__dict__)
                )
            await ms_client.grpc_notify_send_message(
                message_type=SubscribeMessage.SUBSCRIBE_BLOKED,
                user_id=user_id,
                role_descript=tariff.description,
                end_subscribe=role.end_payment
            )       
        roles = await self.crud_billing.get_privileged_roles( 
            filter_status=SubStatusEnum.SUBSCRIBE,
            time_after=timedelta(minutes=1)
        )
        for role in roles:
            user_id, tariff = await self._get_user_and_tariff(role)
            await ms_client.grpc_notify_send_message(
                message_type=SubscribeMessage.SUBSCRIBE_END,
                user_id=user_id,
                role_descript=tariff.description,
                end_subscribe=role.end_payment
            )

    async def _provided_revoked_role(self, provided: bool, payment: PaymentSchema,
                                     role: PrivilegedRoleSchema) -> bool:
        user_id = await self.crud_billing.get_user_id(payment.customer_id)
        tariff = await self.read_marketing.get_role_tariff(payment.role_payment)

        if provided is True:
            await ms_client.grpc_notify_send_message(
                message_type=SubscribeMessage.SUBSCRIBED,
                user_id=user_id,
                role_descript=tariff.description,
                end_subscribe=role.end_payment
            )
            return await rc_client.grpc_auth_provide_role(
                user_id=user_id,
                role_id=tariff.auth_role_id,
                jti=payment.jti_compromised
            )
        await ms_client.grpc_notify_send_message(
            message_type=SubscribeMessage.SUBSCRIBE_BLOKED,
            user_id=user_id,
            role_descript=tariff.description,
            end_subscribe=role.end_payment
        )
        return await rc_client.grpc_auth_revoke_role(
            user_id=user_id,
            role_id=tariff.auth_role_id,
            jti=payment.jti_compromised
        )
    
    def _payment_months(self, subscribe: bool, payment: PaymentSchema, 
                        end_payment: datetime) -> datetime:
        parse_date = end_payment.timetuple()
        year = parse_date.tm_year
        if subscribe is True:
            month = parse_date.tm_mon + payment.amount_months
        else:
            month = parse_date.tm_mon - payment.amount_months
        if month > 12:
            year += 1
            month = month - 12
        if month < 1:
            year -= 1
            month = month + 12
        return end_payment.replace(year=year, month=month, tzinfo=None)

    async def _get_payment_role(self, payment: PaymentSchema
                                ) -> PrivilegedRoleSchema | None:
        roles = await self.crud_billing.get_privileged_roles(
            customer_id=payment.customer_id,
            role=payment.role_payment
        )
        if len(roles) == 0:
            return None
        return roles[0]
    
    async def _get_user_and_tariff(self, role: PrivilegedRoleSchema) -> tuple:
        user_id = await self.crud_billing.get_user_id(role.customer_id)
        tariff = await self.read_marketing.get_role_tariff(role.role_payment)
        return user_id, tariff
    

def subscribe_roles(read_marketing: BaseReadMarketing, crud_billing: BaseCrudBilling
                    ) -> SubscribePrivilegedRoles:
    return SubscribePrivilegedRoles(read_marketing, crud_billing)
