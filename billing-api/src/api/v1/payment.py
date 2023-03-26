from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response
import uuid

from models.request import TestStripe
from models.payment import PaymentUrl
from payment_service.payment_service_abs import BasePaymentService
from payment_service.payment_dependency import get_payment_service

from api.v1.auth import TokenData, authenticate
import api.messages as messages

router = APIRouter()


@router.post(
    '/test',
    response_model=None,
    summary='Test',
    description='test',
    response_description='test',
)
def add_test(
    input: TestStripe = Body(...),
    payment_service: BasePaymentService = Depends(get_payment_service),
    #token_data: TokenData = Depends(authenticate),
) -> None:
    """test."""
    pay = payment_service.get_url_payment(
        amount=input.amount,
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

