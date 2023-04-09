import uuid
from functools import lru_cache
from datetime import datetime

from core.config import settings
from crud_service.read_marketing_abc import BaseReadMarketing
from crud_service.crud_billing_abc import BaseCrudBilling
from payment_service.payment_service_abs import BasePaymentService
from crud_service.crud_dependency import get_crud_billing, get_crud_marketing
from payment_service.payment_dependency import get_payment_service
from schemas.offer_schemas import RoleOffer

class BillingOffer:
    """Privileged roles offer and customer billing."""

    def __init__(self, read_marketing: BaseReadMarketing, crud_billing: BaseCrudBilling, 
                 payment_system: BasePaymentService):
        self.read_marketing = read_marketing
        self.crud_billing = crud_billing
        self.payment_system = payment_system

    async def offer_from_user(self, user_id: uuid.UUID, role_payment: str, 
                              amount_months: int) -> RoleOffer | None:
        """Calculate billing offer."""
        personal_d = await self.read_marketing.get_personal_discount(user_id)
        months_d = await self.read_marketing.get_months_discount(amount_months)
        return await self._calc_offer(
            role_payment=role_payment,
            amount_months=amount_months,
            discount_1=personal_d.discount if personal_d is not None else 0,
            discount_2=months_d.discount if months_d is not None else 0,
        )
    
    async def offer_from_promocode(self, promocode_code: str) -> RoleOffer | None:
        """Calculate billing offer from promocode."""
        promocode = await self.read_marketing.get_promocode_discount(promocode_code)
        if promocode is None:
            return None
        if promocode.expiration < datetime.now().astimezone():
            return None
        return await self._calc_offer(
            role_payment=promocode.role,
            amount_months=promocode.amount_months,
            discount_1=promocode.discount,
            discount_2=0,   
        )
    
    async def _calc_offer(self, role_payment: str, amount_months: int, 
                          discount_1: int, discount_2: int) -> RoleOffer | None:
        role = await self.read_marketing.get_role_tariff(role_payment)
        if role is None:
            return None
        tariff = role.price * amount_months
        tariff_discount = tariff * ((discount_1 + discount_2) / 100)
        total = round((tariff - tariff_discount), settings.payment_smallest_currency)
        return RoleOffer(
            without_discount=tariff,
            discount=tariff_discount,
            total_price=total,
            currency=settings.payment_currency,
            role_payment=role_payment,
            amount_months=amount_months
        )


@lru_cache()
def get_billing_offer() -> BillingOffer:
    return BillingOffer(read_marketing=get_crud_marketing(),
                        crud_billing=get_crud_billing(),
                        payment_system=get_payment_service())
            

