from async_stripe import stripe

from core.config import settings
from payment_service.payment_service_abs import BasePaymentService
from schemas.payment import CheckoutPayment, RefundPayment
from schemas.billing_schemas import PayStatus


stripe.api_key = settings.stripe_api_key


class StripeService(BasePaymentService):
    """Service for interaction with the payment system Stripe."""

    def __init__(self):
        self.currency = settings.payment_currency
        self.smallest_currency = settings.payment_smallest_currency 

    async def create_checkout(self, price: float, client_id: str, 
                              description: str | None = None) -> CheckoutPayment:
        """Return checkout and url payment."""
        checkout = await stripe.checkout.Session.create(            
            line_items=[
                {
                    'price_data': {
                        'currency': self.currency,                        
                        'product_data': {
                            'name': description,
                            'description': description,
                        },
                        'unit_amount': int(price * self.smallest_currency),
                    },
                    'quantity': 1,
                },
            ],
            mode="payment",
            success_url=settings.payment_success_url,
            client_reference_id=client_id,
            currency=self.currency,
        )
        return CheckoutPayment(
            id_checkout=checkout.id,
            url=checkout.url,
            status=PayStatus.BILLED
        )
    
    async def get_checkouts(self, checkout_idx: list[str]
                            ) -> list[CheckoutPayment] | None:
        """Return checkouts list."""
        payment_checkouts = []
        for checkout_id in checkout_idx:
            checkout = await stripe.checkout.Session.retrieve(checkout_id)
            status_checkout = PayStatus.BILLED
            if checkout.status == 'complete':
                status_checkout = PayStatus.PAID
            if checkout.status == 'expired':
                status_checkout = PayStatus.BILLED_TIMEOUT       
            payment_checkouts.append(
                CheckoutPayment(
                    id_checkout=checkout.id,
                    url='https',
                    status=status_checkout,
                    id_payment=str(checkout.payment_intent),
                )    
            )
        return payment_checkouts
    
    async def create_refund_payment(self, payment_id_system: str) -> RefundPayment:
        """Create payment refund."""
        refund = await stripe.Refund.create(payment_intent=payment_id_system)
        return RefundPayment(
            id_refund=str(refund.id),
            status=PayStatus.REFUND
        )
    
    async def get_refunds(self, refunds_idx: list[str]) -> list[RefundPayment] | None:
        """Return refund list."""
        payment_refunds = []
        for refunds_id in refunds_idx:
            refund = await stripe.Refund.retrieve(refunds_id)
            status_refund = PayStatus.REFUND
            if (refund.status == 'pending') | (refund.status == 'succeeded'):
                status_refund = PayStatus.REFUNDED      
            payment_refunds.append(
                RefundPayment(
                    id_refund=str(refund.id),
                    status=status_refund
                )    
            )
        return payment_refunds
