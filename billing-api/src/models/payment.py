from pydantic import BaseModel, UUID4, Field
from datetime import datetime


class PaymentСreate(BaseModel):
    id_pay: str
    card: str
    amount: float
    currency: str


class PaymentUrl(PaymentСreate):
    url_payment: str


