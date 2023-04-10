from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response
import uuid

from schemas.offer_schemas import (QueryOfferRole, ResponseStatusRole, RequestRefund,
                                   RequestPaymentOffer, ResponsePaymentOffer, RoleOffer)
from schemas.billing_schemas import SubStatusEnum, PaymentSchema
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
    offer = await billing.get_offer(
        apply_promocode=query.apply_promocode,
        user_id=user_id,
        role_payment=query.role_payment,
        amount_months=query.amount_months,
        promocode_code=query.promocode,
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
    '/url-payment',
    response_model=ResponsePaymentOffer,
    summary='Url Payment',
    description='Url to pay for a subscription',
    response_description='Url to pay for a subscription',
)
async def get_url_payment(
    body: RequestPaymentOffer = Body(...),
    billing: BillingOffer = Depends(get_billing_offer),
    token_data: TokenData = Depends(authenticate),
) -> ResponsePaymentOffer:
    user_id = uuid.UUID(token_data.user)
    url = await billing.get_payment_url(
        apply_promocode=body.apply_promocode,
        user_id=user_id,
        role_payment=body.role_payment,
        amount_months=body.amount_months,
        promocode_code=body.promocode,
    )
    if url is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.FAULT_BOBY)
    return ResponsePaymentOffer(url_payment=url)


@router.get(
    '/possible-refunds',
    response_model=list[PaymentSchema],
    summary='Possible refunds',
    description='Non-expired payment refund',
    response_description='List payments',
)
async def get_possible_refunds(
    billing: BillingOffer = Depends(get_billing_offer),
    token_data: TokenData = Depends(authenticate)
) -> list[ResponseStatusRole]:
    user_id = uuid.UUID(token_data.user)
    payments = await billing.get_payments_for_refund(user_id)
    if payments is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.USER_NOT_REFUNDS)
    return payments


@router.post(
    '/refund-payment',
    response_model=PaymentSchema,
    summary='Refund payment',
    description='Non-expired payment refund',
    response_description='Update payment',
)
async def refund_payment(
    body: RequestRefund = Body(...),
    billing: BillingOffer = Depends(get_billing_offer),
    token_data: TokenData = Depends(authenticate),
) -> PaymentSchema:
    user_id = uuid.UUID(token_data.user)
    new_payment = await billing.refund_payment(
        user_id=user_id,
        payment_id=body.payment_id,
    )
    if new_payment is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.USER_NOT_REFUNDS)
    return new_payment


@router.post(
    '/check-payments',
    response_model=None,
    summary='Check payments',
    description='Check payments in payment system',
    response_description='Null',
)
async def get_url_payment(
    billing: BillingOffer = Depends(get_billing_offer),
) -> None:
    await billing.check_payments()
    return None