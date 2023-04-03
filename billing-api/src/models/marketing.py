from sqlalchemy import Column, String, UUID, DateTime, Integer, BigInteger, Float

from db.postgresql import Base
  

class PersonalDiscountModel(Base):
    __tablename__ = 'marketing\'.\'personal_discount'

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    user_id = Column(UUID(as_uuid=True), unique=True)
    discount = Column(Integer)


class MonthsDiscountModel(Base):
    __tablename__ = 'marketing\'.\'months_discount'

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    amount_months = Column(Integer)
    discount = Column(Integer)


class PromocodeModel(Base):
    __tablename__ = 'marketing\'.\'promocode'

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    code = Column(String)
    description = Column(String)
    role = Column(String)
    discount = Column(Integer)
    amount_months = Column(Integer)
    expiration = Column(DateTime)


class TariffModel(Base):
    __tablename__ = 'marketing\'.\'tariff'

    id = Column(BigInteger, primary_key=True, default=BigInteger(), unique=True)
    role = Column(String)
    description = Column(String)    
    price = Column(Float)
    