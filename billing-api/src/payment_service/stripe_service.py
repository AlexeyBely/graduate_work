import uuid
import stripe
import logging

from payment_service.payment_service_abs import BasePaymentService
from core.config import settings
from models.payment import PaymentUrl, PaymentСreate


logger = logging.getLogger('')
stripe.api_key = settings.stripe_api_key


class StripeService(BasePaymentService):
    """Service for interaction with the payment system Stripe."""

    def __init__(self):
        self.currency = settings.payment_currency

    def get_url_payment(self, amount: float, description: str | None = None) -> PaymentUrl | None:
        """Get url page and payment details."""
        try:
            checkout = stripe.checkout.Session.create(            
                line_items=[
                    {
                        'price_data': {
                            'currency': settings.payment_currency,
                            #'product': settings.stripe_id_product,                        
                            'product_data': {
                                'name': description,
                                'description': f'user {description}',
                            },
                            'unit_amount': int(amount / settings.stripe_smallest_currency),
                        },
                        'quantity': 1,
                    },
                ],
                mode="payment",
                success_url=settings.payment_success_url,
                client_reference_id='111111-222222-33333',
                currency=settings.payment_currency,
            )
        except Exception as e:
            logger.error(f'{e}')
            return None

        return None
    
    def refund_payment(self):
        """Create payment refund."""
        try:
            refund = stripe.Refund.create(
                payment_intent='pi_3MplK1EDsXu7ZV5D0WClbIxA',
            )
        except Exception as e:
            logger.error(f'{e}')
            return None

        return None
