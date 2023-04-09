from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response
import uuid

from schemas.payment import PaymentUrl
from schemas.offer_schemas import QueryOfferRole, RoleOffer, ResponseStatusRole
from schemas.billing_schemas import SubStatusEnum
from payment_service.payment_service_abs import BasePaymentService
from payment_service.payment_dependency import get_payment_service
from crud_service.crud_billing_abc import BaseCrudBilling
from crud_service.crud_dependency import get_crud_billing
from billing.billing_offer import get_billing_offer, BillingOffer

from api.v1.auth import TokenData, authenticate
import api.messages as messages


router = APIRouter()


@router.get(
    '/offer',
    response_model=RoleOffer,
    summary='Calc offer',
    description='Сalculate offer from discounts or promotional code',
    response_description='Amount with and without discount',
)
async def calc_offer(
    query: QueryOfferRole = Depends(QueryOfferRole),
    billing: BillingOffer = Depends(get_billing_offer),
    token_data: TokenData = Depends(authenticate)
) -> RoleOffer:
    user_id = uuid.UUID(token_data.user)
    if not query.apply_promocode:
        offer = await billing.offer_from_user(
            user_id = user_id, 
            role_payment=query.role_payment,
            amount_months=query.amount_months
        )
    else:
        offer = await billing.offer_from_promocode(
            promocode_code=query.promocode
        )
    if offer is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.FAULT_QUERY)
    return offer


@router.get(
    '/subscrabed-roles',
    response_model=list[ResponseStatusRole],
    summary='Subscrabed roles',
    description='Subscrabed privileded roles',
    response_description='List subscrabed privileded roles',
)
async def privileged_roles(
    crud_billing: BaseCrudBilling = Depends(get_crud_billing),
    token_data: TokenData = Depends(authenticate)
) -> list[ResponseStatusRole]:
    user_id = uuid.UUID(token_data.user)
    customer = await crud_billing.get_customer(user_id)
    if customer is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.USER_NOT_ROLES)
    privil_roles = await crud_billing.get_privileged_roles(
        customer_id=customer.id,
        filter_status=SubStatusEnum.SUBSCRIBE
    )
    if privil_roles is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.USER_NOT_ROLES)    
    roles_response = [ResponseStatusRole(**role.__dict__) for role in privil_roles]
    return roles_response
    


@router.post(
    '/test',
    response_model=None,
    summary='Test',
    description='test',
    response_description='test',
)
def add_test(
    payment_service: BasePaymentService = Depends(get_payment_service),
    #token_data: TokenData = Depends(authenticate),
) -> None:
    """test."""
    pay = payment_service.get_url_payment(
        amount=100,
        description='test pay',
    )
    return None


@router.post(
    '/refund',
    response_model=None,
    summary='Test',
    description='test',
    response_description='test',
)
def add_test_test(
    payment_service: BasePaymentService = Depends(get_payment_service),
    #token_data: TokenData = Depends(authenticate),
) -> None:
    """test."""
    pay = payment_service.refund_payment()
    return None

