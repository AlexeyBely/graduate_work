from pydantic import BaseModel, UUID4
from datetime import datetime


class PersonalDiscountSchema(BaseModel):
    user_id: UUID4
    discount: int


class MonthsDiscountSchema(BaseModel):
    amount_months: int
    discount: int


class PromocodeSchema(BaseModel):
    code: str
    description: str | None
    role: str
    discount: int
    amount_months: int
    expiration: datetime


class TariffSchema(BaseModel):
    role: str
    description: str | None   
    price: float
    auth_role_id: UUID4
