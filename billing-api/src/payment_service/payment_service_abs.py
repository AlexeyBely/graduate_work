from abc import ABC, abstractmethod
import uuid

from schemas.payment import CheckoutPayment, RefundPayment


class BasePaymentService(ABC):
    """Service for interaction with the payment system Stripe."""

    @abstractmethod
    async def create_checkout(self, price: float, client_id: str, 
                              description: str | None = None) -> CheckoutPayment:
        """Return checkout and url payment."""
        pass

    @abstractmethod
    async def get_checkouts(self, checkout_idx: list[str]
                            ) -> list[CheckoutPayment] | None:
        """Return checkouts list."""
        pass
    
    @abstractmethod
    async def create_refund_payment(self, payment_id_system: str) -> RefundPayment:
        """Create payment refund."""
        pass

    @abstractmethod
    async def get_refunds(self, refunds_idx: list[str]) -> list[RefundPayment] | None:
        """Return refund list."""
        pass
