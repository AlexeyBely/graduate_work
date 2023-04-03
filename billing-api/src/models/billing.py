import uuid
import enum
from sqlalchemy import Column, String, UUID, DateTime, Integer, Float, Enum, ForeignKey

from db.postgresql import Base
  

class SubscriptionStatus(enum.Enum):
    CREATED = 'created'
    SUBSCRIBE = 'subscribe'
    EXPIRED = 'expired'
    BLOCKED = 'blocked'


class PaymentStatus(enum.Enum):
    BILLED = 'billed'
    PAID = 'paid'
    BILLED_TIMEOUT = 'billed_timeout'
    REFUND = 'refund'
    REFUNDED = 'refunded'


class CustomerModel(Base):
    __tablename__ = 'billing\'.\'customer'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    id_user = Column(UUID(as_uuid=True), unique=True)
    email = Column(String)


class PrivilegedRoleModel(Base):
    __tablename__ = 'billing\'.\'privileged_role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    customer = Column(UUID(as_uuid=True), ForeignKey('customer.id'))
    status = Column(Enum(SubscriptionStatus))
    role_payment = Column(String)
    end_payment = Column(DateTime)


class PaymentModel(Base):
    __tablename__ = 'billing\'.\'payment'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    customer = Column(UUID(as_uuid=True), ForeignKey('customer.id'))
    status = Column(Enum(PaymentStatus))
    role_payment = Column(String)
    amount_months = Column(Integer)
    payed_at = Column(DateTime)
    personal_discount = Column(Integer)
    months_discount = Column(Integer)
    promocode = Column(String)
    tariff = Column(Float)
    amount = Column(Float)
    currency = Column(String)
    id_payment = Column(String)
    id_checkout = Column(String)
    id_refund = Column(String)
    card = Column(String)
