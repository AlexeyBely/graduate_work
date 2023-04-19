import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

import api.messages as messages
from api.v1.auth import TokenData, authenticate
from crud_service.crud_dependency import get_crud_marketing
from crud_service.read_marketing_abc import BaseReadMarketing
from schemas.marketing_schemas import (MonthsDiscountSchema,
                                       PersonalDiscountSchema, TariffSchema)

router = APIRouter()


@router.get(
    '/tariffs',
    response_model=list[TariffSchema],
    summary='Tariffs list',
    description='All tariffs list',
    response_description='Response tariffs list',
)
async def get_tariffs(
    crud_marketing: BaseReadMarketing = Depends(get_crud_marketing),
) -> list[TariffSchema]:
    tariffs = await crud_marketing.get_tariffs()
    if tariffs is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,  
                            detail=messages.TARIFFS_NOT_CREATED)
    return tariffs


@router.get(
    '/months-discounts',
    response_model=list[MonthsDiscountSchema],
    summary='Months discounts list',
    description='All months discounts list',
    response_description='Response months discounts list',
)
async def get_months_discounts(
    crud_marketing: BaseReadMarketing = Depends(get_crud_marketing),
) -> list[MonthsDiscountSchema]:
    discounts = await crud_marketing.get_months_discounts()
    if discounts is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,  
                            detail=messages.DISCOUNTS_NOT_CREATED)
    return discounts


@router.get(
    '/personal-discount',
    response_model=PersonalDiscountSchema,
    summary='Personal discount',
    description='Personal discount for the user specified in the token',
    response_description='Personal discount',
)
async def get_personal_discount(
    crud_marketing: BaseReadMarketing = Depends(get_crud_marketing),
    token_data: TokenData = Depends(authenticate)
) -> PersonalDiscountSchema:
    user_id = uuid.UUID(token_data.user)
    discount = await crud_marketing.get_personal_discount(user_id)
    if discount is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,  
                            detail=messages.USER_NOT_DISCOUNT)
    return discount
