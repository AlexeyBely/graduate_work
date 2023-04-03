from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response
import uuid

from schemas.payment import PaymentUrl
from payment_service.payment_service_abs import BasePaymentService
from payment_service.payment_dependency import get_payment_service

from api.v1.auth import TokenData, authenticate
import api.messages as messages

router = APIRouter()