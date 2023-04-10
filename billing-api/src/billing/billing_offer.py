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
from schemas.billing_schemas import (CustomerSchema, CustomerBase, PaymentBase, 
                                     PayStatus, PaymentSchema)

class BillingOffer:
    """Privileged roles offer and customer billing."""

    def __init__(self, read_marketing: BaseReadMarketing, crud_billing: BaseCrudBilling, 
                 payment_system: BasePaymentService):
        self.read_marketing = read_marketing
        self.crud_billing = crud_billing
        self.payment_system = payment_system

    async def get_offer(self, apply_promocode: bool, user_id: uuid.UUID, 
                        role_payment: str, amount_months: int, promocode_code: str
                        ) -> RoleOffer | None:
        """Offer for personal and monthly discounts or promocode."""
        if not apply_promocode:
            offer = await self.offer_from_user(
                user_id = user_id, 
                role_payment=role_payment,
                amount_months=amount_months
            )
        else:
            offer = await self.offer_from_promocode(
                promocode_code=promocode_code
            )
        return offer


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
            amount_months=amount_months,
            personal_percent=discount_1,
            month_percent=discount_2,
            role_description=role.description
        )
    
    async def get_payment_url(self, apply_promocode: bool, user_id: uuid.UUID, 
                              role_payment: str, amount_months: int, promocode_code: str
                             ) -> str | None:
        """Return url payment and create object payment in billing service."""
        offer = await self.get_offer(
            apply_promocode=apply_promocode,
            user_id=user_id,
            role_payment=role_payment,
            amount_months=amount_months,
            promocode_code=promocode_code,
        )
        if offer is None:
            return None
        checkout = await self.payment_system.create_checkout(
            price=offer.total_price,
            client_id=str(user_id),
            description='Subscribe {0} for {1} months'.format(
                offer.role_description,
                offer.amount_months,    
            )
        )
        customer = await self._get_or_create_customer(user_id)
        await self.crud_billing.create_payment(
            PaymentBase(
                customer_id=customer.id,
                status=PayStatus.BILLED,
                role_payment=offer.role_payment,
                amount_months=offer.amount_months,
                payed_at=datetime.now(),
                personal_discount=offer.personal_percent,
                months_discount=offer.month_percent,
                promocode=promocode_code if apply_promocode is True else None,
                tariff=offer.without_discount,
                amount=offer.total_price,
                currency=offer.currency,
                id_checkout=checkout.id_checkout,
            )
        )
        return checkout.url
    
    async def check_payments(self) -> None:
        """Checks payment of users in the payment system."""
        # check paid
        billed_payments = await self.crud_billing.get_payments(
            filter_status=PayStatus.BILLED
        )
        checkout_idx = [pay.id_checkout for pay in billed_payments]
        checkouts = await self.payment_system.get_checkouts(checkout_idx)
        payment_counter = 0
        for checkout in checkouts:
            if checkout.status == PayStatus.PAID:
                payment = billed_payments[payment_counter]
                #update role ______________-
                payment.status = PayStatus.PAID
                payment.payed_at=datetime.now()
                payment.id_payment = checkout.id_payment
                await self.crud_billing.update_payment(
                    payment_id=payment.id,
                    payment=PaymentBase(**payment.__dict__)
                )
                payment_counter += 1
        # check refunded
        refund_payments = await self.crud_billing.get_payments(
            filter_status=PayStatus.REFUND
        )
        refund_idx = [pay.id_refund for pay in refund_payments]
        refunds = await self.payment_system.get_refunds(refund_idx)
        payment_counter = 0
        for refund in refunds:
            if refund.status == PayStatus.REFUNDED:
                payment = refund_payments[payment_counter]
                #update role ______________-
                payment.status = PayStatus.REFUNDED
                await self.crud_billing.update_payment(
                    payment_id=payment.id,
                    payment=PaymentBase(**payment.__dict__)
                )
                payment_counter += 1

    async def get_payments_for_refund(self, user_id: uuid.UUID
                                      ) -> list[PaymentSchema] | None:
        """List of payments for a possible refund."""
        customer = await self.crud_billing.get_customer(user_id)
        if customer is None:
            return None
        payments = await self.crud_billing.get_payments(
            customer_id=customer.id,
            filter_status=PayStatus.PAID,
            hours_passed=settings.payment_hours_refund
        )
        return payments
    
    async def refund_payment(self, user_id: uuid.UUID, payment_id: uuid.UUID
                             ) -> PaymentSchema | None:
        """Refund payment if passible."""
        payments_passible = await self.get_payments_for_refund(user_id)
        passible = False
        for payment in payments_passible:
            if payment.id == payment_id:
                passible = True
                break   
        if passible is not True:
            return None
        refund = await self.payment_system.create_refund_payment(payment.id_payment)
        payment.status = PayStatus.REFUND
        payment.id_refund = refund.id_refund
        new_payment = await self.crud_billing.update_payment(
            payment_id=payment.id,
            payment=PaymentBase(**payment.__dict__)
        )
        return new_payment

    async def _get_or_create_customer(self, user_id: uuid.UUID) -> CustomerSchema:
        customer = await self.crud_billing.get_customer(user_id)
        if customer is None:
            # Here read email user
            email = 'debag@mail.com'
            # ---------------------
            customer = await self.crud_billing.create_customer(
                CustomerBase(
                    user_id=user_id,
                    email=email,
                )
            )
        return customer 


@lru_cache()
def get_billing_offer() -> BillingOffer:
    return BillingOffer(read_marketing=get_crud_marketing(),
                        crud_billing=get_crud_billing(),
                        payment_system=get_payment_service())
            

