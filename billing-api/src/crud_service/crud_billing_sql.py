import uuid
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from crud_service.crud_billing_abc import BaseCrudBilling
from models.billing import CustomerModel, PaymentModel, PrivilegedRoleModel
from schemas.billing_schemas import (CustomerBase, CustomerSchema, PaymentBase,
                                     PaymentSchema, PayStatus,
                                     PrivilegedRoleBase, PrivilegedRoleSchema,
                                     SubStatusEnum)


class SqlCrudBilling(BaseCrudBilling):
    """CRUD from schema billing database."""

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session
    
    # Methods for customer
    async def create_customer(self, customer_data: CustomerBase) -> CustomerSchema:
        """Create customer with user_id and email."""
        async with self.async_session() as session:
            insert_obj = CustomerModel(**customer_data.__dict__)
            async with session.begin():
                session.add(insert_obj)
            return CustomerSchema(**insert_obj.__dict__)
        
    async def get_customer(self, user_id: uuid.UUID) -> CustomerSchema | None:
        """Read customer with user_id."""
        async with self.async_session() as session:
            customer = await self._execute_customer(session, user_id)
            if customer is None:
                return None
            return CustomerSchema(**customer.__dict__)
        
    async def update_email_customer(self, user_id: uuid.UUID, email: str
                                    ) -> CustomerSchema | None:
        """Update customer with user_id and email."""
        async with self.async_session() as session:
            customer = await self._execute_customer(session, user_id)
            if customer is None:
                return None
            customer.email = email
            await session.commit()
            return CustomerSchema(**customer.__dict__)
        
    async def delete_customer(self, user_id: uuid.UUID) -> None:
        """Delete customer with user_id."""
        async with self.async_session() as session:
            customer = await self._execute_customer(session, user_id)
            await session.delete(customer)
            await session.commit()

    async def get_user_id(self, customer_id: uuid.UUID) -> uuid.UUID | None:
        """Read user_id with customer_id."""
        customer = await self._read_obj(CustomerModel, CustomerSchema, customer_id)
        return customer.user_id

    # Methods for payment
    async def create_payment(self, payment: PaymentBase) -> PaymentSchema:
        """Create new payment."""
        return await self._create_obj(PaymentModel, PaymentSchema, payment)

    async def get_payment(self, payment_id: uuid.UUID) -> PaymentSchema | None:
        """Read payment with payment_id."""
        return await self._read_obj(PaymentModel, PaymentSchema, payment_id)
    
    async def update_payment(self, payment_id: uuid.UUID, payment: PaymentBase
                             ) -> PaymentSchema:
        """Update payment with payment_id."""
        return await self._update_obj(PaymentModel, PaymentSchema, payment_id, payment)
    
    async def delete_payment(self, payment_id: uuid.UUID) -> None:
        """Delete payment with payment_id."""
        return await self._delete_obj(PaymentModel, payment_id)
    
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
        async with self.async_session() as session:
            stmt = select(PaymentModel)
            if customer_id is not None:
                stmt = stmt.where(PaymentModel.customer_id == customer_id)
            if filter_status is not None:
                stmt = stmt.where(PaymentModel.status == filter_status)
            if hours_passed is not None:
                check_time = datetime.now() - timedelta(hours=hours_passed)
                stmt = stmt.where(PaymentModel.payed_at > check_time)
            result = await session.execute(stmt.order_by(PaymentModel.payed_at))
            payments = result.scalars().all()
            if payments is None:
                return None
            return [PaymentSchema(**pay.__dict__) for pay in payments]

    # Methods for privileged role
    async def create_privileged_role(self, privel_role: PrivilegedRoleBase
                                     ) -> PrivilegedRoleSchema:
        """Create new privileged role."""
        return await self._create_obj(PrivilegedRoleModel, PrivilegedRoleSchema, 
                                      privel_role)

    async def get_privileged_role(self, privel_role_id: uuid.UUID
                                  ) -> PrivilegedRoleSchema | None:
        """Read privileged role at id."""
        return await self._read_obj(PrivilegedRoleModel, PrivilegedRoleSchema, 
                                    privel_role_id)
    
    async def update_privileged_role(self, 
                                     privel_role_id: uuid.UUID, 
                                     privel_role: PrivilegedRoleBase
                                     ) -> PrivilegedRoleSchema:
        """Update privileged role at id."""
        return await self._update_obj(PrivilegedRoleModel, PrivilegedRoleSchema, 
                                      privel_role_id, privel_role)
    
    async def delete_privileged_role(self, privel_role_id: uuid.UUID) -> None:
        """Delete privileged role at id."""
        return await self._delete_obj(PrivilegedRoleModel, privel_role_id)
    
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
        async with self.async_session() as session:
            stmt = select(PrivilegedRoleModel)
            if customer_id is not None:
                stmt = stmt.where(PrivilegedRoleModel.customer_id == customer_id)
            if filter_status is not None:
                stmt = stmt.where(PrivilegedRoleModel.status == filter_status)
            if time_after is not None:
                check_time = datetime.now() - time_after
                stmt = stmt.where(PrivilegedRoleModel.end_payment < check_time)
            if role is not None:
                stmt = stmt.where(PrivilegedRoleModel.role_payment == role)
            result = await session.execute(
                stmt.order_by(PrivilegedRoleModel.end_payment)
            )
            privil_roles = result.scalars().all()
            if privil_roles is None:
                return None
            return [PrivilegedRoleSchema(**role.__dict__) for role in privil_roles]

    # Utils methods    
    async def _execute_customer(self, session: AsyncSession, user_id: uuid.UUID
                                ) -> CustomerModel | None:
        stmt = select(CustomerModel).where(CustomerModel.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    
    async def _create_obj(self, model, schema, data_schema):
        async with self.async_session() as session:
            insert_obj = model(**data_schema.__dict__)
            async with session.begin():
                session.add(insert_obj)
            return schema(**insert_obj.__dict__)
        
    async def _read_obj(self, model, schema, obj_id):
        async with self.async_session() as session:
            stmt = select(model).where(model.id == obj_id)
            result = await session.execute(stmt)
            model_obj = result.scalars().first()
            if model_obj is None:
                return None
            return schema(**model_obj.__dict__)
        
    async def _update_obj(self, model, schema, obj_id, data_schema):
        async with self.async_session() as session:
            stmt = select(model).where(model.id == obj_id)
            result = await session.execute(stmt)
            model_obj = result.scalars().one()
            for key, value in data_schema.__dict__.items():
                setattr(model_obj, key, value)
            await session.commit()
            return schema(**model_obj.__dict__)
        
    async def _delete_obj(self, model, obj_id):
        async with self.async_session() as session:
            stmt = select(model).where(model.id == obj_id)
            result = await session.execute(stmt)
            model_obj = result.scalars().one()
            await session.delete(model_obj)
            await session.commit()
