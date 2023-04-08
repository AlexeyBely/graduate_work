import uuid
from datetime import datetime, timedelta

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response

from schemas.billing_schemas import (CustomerBase, CustomerSchema, PaymentBase, PaymentSchema,
                                     PrivilegedRoleBase, PrivilegedRoleSchema)
from crud_service.crud_billing_abc import BaseCrudBilling
from crud_service.crud_dependency import get_crud_billing
from api.v1.auth import TokenData, authenticate
import api.messages as messages


router = APIRouter()


@router.post(
    '/customer',
    response_model=list[PrivilegedRoleSchema],
    summary='test',
    description='test',
    response_description='test',
)
async def create_user(
    crud_billing: BaseCrudBilling = Depends(get_crud_billing),
) -> list[PrivilegedRoleSchema]:
    flag = True
    if flag is True:
        cust = await crud_billing.get_privileged_roles(
            filter_status='subscribe',
            #customer_id=uuid.UUID('403aebd3-af49-4d87-8875-869c4bf65208'),
            time_after=timedelta(days=2),
        )
    else:
        cust = await crud_billing.delete_privileged_role(
            privel_role_id=uuid.UUID('403aebd3-af49-4d87-8875-869c4bf65208'),   
        )
    if not cust:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,  
                            detail=messages.TARIFFS_NOT_CREATED)
    return cust