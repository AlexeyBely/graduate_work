from abc import ABC, abstractmethod
import uuid

from schemas.payment import PaymentUrl


class BasePaymentService(ABC):
    @abstractmethod
    def get_url_payment(self, 
                        amount: float, 
                        description: str | None = None
                        ) -> PaymentUrl | None:
        """Get url page and payment details."""
        pass

    def refund_payment(self):
        """Create payment refund."""
        pass

