import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from schemas.billing_schemas import (CustomerSchema, PrivilegedRoleSchema,
                                     PaymentSchema, PayStatus, SubStatusEnum,
                                     CustomerBase, PrivilegedRoleBase, PaymentBase)


class BaseCrudBilling(ABC):
    """CRUD from schema billing database."""
    
    @abstractmethod
    async def create_customer(self, customer_data: CustomerBase) -> CustomerSchema:
        """Create customer with user_id and email."""
        pass

    @abstractmethod
    async def get_customer(self, user_id: uuid.UUID) -> CustomerSchema | None:
        """Read customer with user_id."""
        pass

    @abstractmethod
    async def update_email_customer(self, user_id: uuid.UUID, email: str
                                    ) -> CustomerSchema | None:
        """Update customer with user_id and email."""
        pass

    @abstractmethod
    async def delete_customer(self, user_id: uuid.UUID) -> None:
        """Delete customer with user_id."""
        pass

    @abstractmethod
    async def create_payment(self, payment: PaymentBase) -> PaymentSchema:
        """Create new payment."""
        pass  

    @abstractmethod
    async def get_payment(self, payment_id: uuid.UUID) -> PaymentSchema | None:
        """Read payment with payment_id."""
        pass

    @abstractmethod
    async def update_payment(self, payment_id: uuid.UUID, payment: PaymentBase
                             ) -> PaymentSchema:
        """Update payment with payment_id."""
        pass

    @abstractmethod
    async def delete_payment(self, payment_id: uuid.UUID) -> None:
        """Delete payment with payment_id."""
        pass

    @abstractmethod
    async def get_payments(self,
                           customer_id: uuid.UUID | None = None, 
                           filter_status: PayStatus | None = None,
                           hours_passed: int | None = None
                           ) -> list[PaymentSchema] | None:
        """Read payments meeting the following filters.

        - customer_id - id customer,
        - filter_status - payment status at the moment,
        - hours_passed - fewer hours have passed since payment. 
        """
        pass

    @abstractmethod
    async def create_privileged_role(self, privel_role: PrivilegedRoleBase
                                     ) -> PrivilegedRoleSchema:
        """Create new privileged role."""
        pass

    @abstractmethod
    async def get_privileged_role(self, privel_role_id: uuid.UUID
                                  ) -> PrivilegedRoleSchema | None:
        """Read privileged role at id."""
        pass

    @abstractmethod
    async def update_privileged_role(self, 
                                     privel_role_id: uuid.UUID, 
                                     privel_role: PrivilegedRoleBase
                                     ) -> PrivilegedRoleSchema:
        """Update privileged role at id."""
        pass

    @abstractmethod
    async def delete_privileged_role(self, privel_role_id: uuid.UUID) -> None:
        """Delete privileged role at id."""
        pass

    @abstractmethod
    async def get_privileged_roles(self,
                                   customer_id: uuid.UUID | None = None,
                                   filter_status: SubStatusEnum | None = None,
                                   time_after: datetime | None = None,
                                   role: str | None = None,                                 
                                   ) -> list[PrivilegedRoleSchema] | None:
        """Read privileged roles meeting the following filters.

        - customer_id - id customer,
        - filter_status - subscription status on privileged roles,
        - time_after_expired - more time has passed since the subscription expired. 
        """
        pass

    @abstractmethod
    async def get_user_id(self, customer_id: uuid.UUID) -> uuid.UUID | None:
        """Read user_id with customer_id."""
        pass