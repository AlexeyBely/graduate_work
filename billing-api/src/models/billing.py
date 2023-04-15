import uuid
from sqlalchemy import Column, String, UUID, DateTime, Integer, Float, ForeignKey 
from db.psql_async import Base


class CustomerModel(Base):
    __tablename__ = 'customer'
    __table_args__ = {'schema': 'billing'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(UUID(as_uuid=True), unique=True)
    email = Column(String)


class PrivilegedRoleModel(Base):
    __tablename__ = 'privileged_role'
    __table_args__ = {'schema': 'billing'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('billing.customer.id'))
    status = Column(String)
    role_payment = Column(String)
    end_payment = Column(DateTime)


class PaymentModel(Base):
    __tablename__ = 'payment'
    __table_args__ = {'schema': 'billing'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('billing.customer.id'))
    status = Column(String)
    role_payment = Column(String)
    amount_months = Column(Integer)
    payed_at = Column(DateTime)
    personal_discount = Column(Integer, nullable=True)
    months_discount = Column(Integer, nullable=True)
    promocode = Column(String, nullable=True)
    tariff = Column(Float)
    amount = Column(Float)
    currency = Column(String)
    id_payment = Column(String, nullable=True)
    id_checkout = Column(String, nullable=True)
    id_refund = Column(String, nullable=True)
    card = Column(String, nullable=True)
    jti_compromised = Column(String, nullable=True)
