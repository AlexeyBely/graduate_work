import uuid
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import UUID, desc

from schemas.marketing_schemas import (TariffSchema, PersonalDiscountSchema, 
                                       MonthsDiscountSchema, PromocodeSchema)
from crud_service.read_marketing_abc import BaseReadMarketing
from models.marketing import (TariffModel, PersonalDiscountModel,
                              MonthsDiscountModel, PromocodeModel)


class SqlReadMarketing(BaseReadMarketing):
    """Reading from schema marketing sql database."""
    
    def __init__(self, session: Session):
        self.session = session

    async def get_tariffs(self) -> list[TariffSchema] | None:
        """Read tariff plans as privileged roles."""
        result = await self.session.execute(select(TariffModel))  # type: ignore
        tariffs = result.scalars().all()
        if tariffs is None:
            return None
        return [TariffSchema(**tariff.__dict__) for tariff in tariffs]
    
    async def get_role_tariff(self, role: str) -> TariffSchema | None:
        """Read privileged role tariff."""
        stmt = select(TariffModel).where(TariffModel.role == role)
        result = await self.session.execute(stmt)
        tariff = result.scalars().first()
        if tariff is None:
            return None
        return TariffSchema(**tariff.__dict__)
    
    async def get_personal_discount(self, user_id: uuid.UUID
                                    ) -> PersonalDiscountSchema | None:
        """Read personal discount at user_id."""
        stmt = select(PersonalDiscountModel).where(PersonalDiscountModel.user_id
                                                    == user_id)
        result = await self.session.execute(stmt)
        discount = result.scalars().first()
        if discount is None:
            return None
        return PersonalDiscountSchema(**discount.__dict__)
    
    async def get_months_discounts(self) -> list[MonthsDiscountSchema] | None:
        """Read months discounts."""
        result = await self.session.execute(select(MonthsDiscountModel))
        discounts = result.scalars().all()
        if discounts is None:
            return None
        return [MonthsDiscountSchema(**discount.__dict__) for discount in discounts]
    

    async def get_months_discount(self, amount_months: int
                                  ) -> MonthsDiscountSchema | None:
        """Read discount at amount months."""
        stmt = select(MonthsDiscountModel).where(MonthsDiscountModel.amount_months
            <= amount_months).order_by(desc(MonthsDiscountModel.amount_months))
        result = await self.session.execute(stmt)
        discount = result.scalars().first()
        if discount is None:
            return None
        return MonthsDiscountSchema(**discount.__dict__)

    async def get_promocode_discount(self, promocode: str) -> PromocodeSchema | None:
        """Read discount at promocode."""
        stmt = select(PromocodeModel).where(PromocodeModel.code == promocode)
        result = await self.session.execute(stmt)
        promocode = result.scalars().first()
        if promocode is None:
            return None
        return PromocodeSchema(**promocode.__dict__)    
