from functools import lru_cache

from payment_service.stripe_service import StripeService


@lru_cache()
def get_payment_service() -> StripeService:
    """interface payment system."""
    return StripeService()
