from pydantic import BaseModel, Field, UUID4
from fastapi import Query
from datetime import datetime


class QueryOfferRole(BaseModel):
    apply_promocode: bool = Query(
        False, 
        description='Offer to promocode or tariff and discounts'
    )
    role_payment: str = Query('you_role', description='Purchasable privileged role')
    amount_months: int = Query(1, description='Purchased number of months', ge=1, le=12)
    promocode: str = Query('code', description='promo code, not required')


class RoleOffer(BaseModel):
    without_discount: float
    discount: float
    total_price: float
    currency: str
    role_payment: str
    amount_months: int
    personal_percent: int
    month_percent: int
    role_description: str


class ResponseStatusRole(BaseModel):
    role_payment: str
    end_payment: datetime


class RequestPaymentOffer(BaseModel):
    apply_promocode: bool = Field(
        False, 
        description='Offer to promocode or tariff and discounts'
    )
    role_payment: str = Field('you_role', description='Purchasable privileged role')
    amount_months: int = Field(1, description='Purchased number of months', ge=1, le=12)
    promocode: str = Field('code', description='promo code, not required')


class ResponsePaymentOffer(BaseModel):
    url_payment: str


class RequestRefund(BaseModel):
    payment_id: UUID4 = Field('xxxxxxxx-xxxx-Mxxx-Nxxx-xxxxxxxxxxxx', 
                              description='ID payment')
