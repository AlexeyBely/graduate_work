from pydantic import BaseModel
from datetime import datetime

from schemas.billing_schemas import PayStatus


class CheckoutPayment(BaseModel):
    id_checkout: str
    id_payment: str | None = None    
    card: str | None = None
    url: str
    status: PayStatus


class RefundPayment(BaseModel):
    id_refund: str
    status: PayStatus



