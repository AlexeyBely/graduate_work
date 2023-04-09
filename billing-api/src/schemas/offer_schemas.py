from pydantic import BaseModel, Field
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


class ResponseStatusRole(BaseModel):
    role_payment: str
    end_payment: datetime

