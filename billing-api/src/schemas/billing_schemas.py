from pydantic import BaseModel, UUID4, EmailStr
from datetime import datetime
from enum import Enum


class SubStatusEnum(str, Enum):
    CREATED = 'created'
    SUBSCRIBE = 'subscribe'
    EXPIRED = 'expired'
    BLOCKED = 'blocked'


class PayStatus(str, Enum):
    BILLED = 'billed'
    PAID = 'paid'
    BILLED_TIMEOUT = 'billed_timeout'
    REFUND = 'refund'
    REFUNDED = 'refunded'


class CustomerBase(BaseModel):    
    user_id: UUID4
    email: EmailStr 


class PrivilegedRoleBase(BaseModel):
    customer_id: UUID4
    status: SubStatusEnum
    role_payment: str
    end_payment: datetime


class PaymentBase(BaseModel):
    customer_id: UUID4
    status: PayStatus
    role_payment: str
    amount_months: int
    payed_at: datetime
    personal_discount: int | None
    months_discount: int | None
    promocode: str | None
    tariff: float
    amount: float
    currency: str
    id_payment: str | None
    id_checkout: str | None
    id_refund: str | None
    card: str | None


class MixinId(BaseModel):    
    id: UUID4

    class Config:
        orm_mode = True


class CustomerSchema(CustomerBase, MixinId):
    pass 


class PrivilegedRoleSchema(PrivilegedRoleBase, MixinId):
    pass


class PaymentSchema(PaymentBase, MixinId):
    pass