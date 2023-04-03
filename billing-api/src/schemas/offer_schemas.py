from pydantic import BaseModel, Field, UUID4
from fastapi import Query
from datetime import datetime


class RequestOfferRole(BaseModel):
    role_payment: str = Field('you_role', description='Purchasable privileged role')
    amount_months: int = Field(1, description='Purchased number of months', ge=1, le=12)


class RequestOfferPromocode(BaseModel):
    promocode: str = Field('code', description='promo code, not required')


class ResponseOffer(RequestOfferRole):
    without_discount: float = Field(1, description='Price without discount')
    discount: float = Field(1, description='Discount')
    total_price: float = Field(1, description='Discounted price')
    currency: str = Field('usd', description='Currency')


class StatusRole(BaseModel):
    role_payment: str
    end_payment: datetime


class ResponseStatusRoles(BaseModel):
    payment_roles: list[StatusRole]
