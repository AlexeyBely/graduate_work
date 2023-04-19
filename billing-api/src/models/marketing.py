from sqlalchemy import (UUID, BigInteger, Column, DateTime, Float, Integer,
                        String)

from db.psql_async import Base


class PersonalDiscountModel(Base):
    __tablename__ = 'personal_discount'
    __table_args__ = {'schema': 'marketing'}

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    user_id = Column(UUID(as_uuid=True), unique=True)
    discount = Column(Integer)


class MonthsDiscountModel(Base):
    __tablename__ = 'months_discount'
    __table_args__ = {'schema': 'marketing'}

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    amount_months = Column(Integer)
    discount = Column(Integer)


class PromocodeModel(Base):
    __tablename__ = 'promocode'
    __table_args__ = {'schema': 'marketing'}

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    code = Column(String)
    description = Column(String, nullable=True)
    role = Column(String)
    discount = Column(Integer)
    amount_months = Column(Integer)
    expiration = Column(DateTime)


class TariffModel(Base):
    __tablename__ = 'tariff'
    __table_args__ = {'schema': 'marketing'}

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    role = Column(String)
    description = Column(String, nullable=True)    
    price = Column(Float)
    auth_role_id = Column(UUID(as_uuid=True), unique=True)
