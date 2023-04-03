import uuid
from abc import ABC, abstractmethod

from schemas.marketing_schemas import (TariffSchema, PersonalDiscountSchema, 
                                       MonthsDiscountSchema, PromocodeSchema)


class BaseReadMarketing(ABC):
    """Reading from schema marketing database."""
    
    @abstractmethod
    async def get_tariffs(self) -> list[TariffSchema] | None:
        """Read tariff plans as privileged roles."""
        pass

    @abstractmethod
    async def get_role_tariff(self, role: str) -> TariffSchema | None:
        """Read privileged role tariff."""
        pass

    @abstractmethod
    async def get_personal_discount(self, user_id: uuid.UUID
                                    ) -> PersonalDiscountSchema | None:
        """Read personal discount at user_id."""
        pass

    @abstractmethod
    async def get_months_discounts(self) -> list[MonthsDiscountSchema] | None:
        """Read months discounts."""
        pass

    @abstractmethod
    async def get_months_discount(self, amount_months: int
                                  ) -> MonthsDiscountSchema | None:
        """Read discount at amount months."""
        pass

    @abstractmethod
    async def get_promocode_discount(self, promocode: str) -> PromocodeSchema | None:
        """Read discount at promocode."""
        pass
