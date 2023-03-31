import uuid
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


MAX_LENGTH_NAME = 255


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
    

class PrivilegedRole(UUIDMixin):
    """State and end of privileged role.""" 

    class SubscriptionStatus(models.TextChoices):
        CREATED = 'created', _('created')
        SUBSCRIBE = 'subscribe', _('subscribe')
        EXPIRED = 'expired', _('expired')
        BLOCKED = 'blocked', _('blocked')

    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=_('customers')
    )
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=SubscriptionStatus.choices,
    )
    role_payment = models.CharField(_('Role'), max_length=MAX_LENGTH_NAME)
    end_payment = models.DateTimeField(_('End payment'))

    class Meta:
        db_table = 'billing\'.\'privileged_role'
        verbose_name = _('privileged_role')
        verbose_name_plural = _('privileged_roles')
        constraints = [
            models.UniqueConstraint(
                fields=['customer_id',],
                name="customer_role_idx"
            ),
        ]

    def __str__(self):
        return self.role_payment
    

class Payment(UUIDMixin):
    """Status and payment details.""" 

    class PaymentStatus(models.TextChoices):
        BILLED = 'billed', _('billed')
        PAID = 'paid', _('paid')
        BILLED_TIMEOUT = 'billed_timeout', _('billed_timeout')
        REFUND = 'refund', _('refund')
        REFUNDED = 'refunded', _('refunded')

    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=_('customers')
    )
    status = models.CharField(
        _('Status'),
        max_length=15,
        choices=PaymentStatus.choices,
    )
    role_payment = models.CharField(_('Role'), max_length=MAX_LENGTH_NAME)
    amount_months = models.IntegerField(_('Months'))
    payed_at = models.DateTimeField(_('Payed'))
    personal_discount = models.IntegerField(_('Personal discount'))
    months_discount = models.IntegerField(_('Months discount'))
    promocode = models.CharField(_('Promocode'), max_length=MAX_LENGTH_NAME)
    tariff = models.FloatField(_('Price'))
    amount = models.FloatField(_('Amount'))
    currency = models.CharField(_('Currency'), max_length=MAX_LENGTH_NAME)
    id_payment = models.TextField('id_payment')
    id_checkout = models.TextField('id_checkout')
    id_refund = models.TextField('id_refund')
    card = models.TextField('card')

    class Meta:
        db_table = 'billing\'.\'payment'
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        constraints = [
            models.UniqueConstraint(
                fields=['customer_id',],
                name="customer_payment_idx"
            ),
        ]

    def __str__(self):
        return str(f'{self.amount} {self.currency}')
    

class Customer(UUIDMixin):
    """User bound client."""
    user_id = models.UUIDField(_('ID_user'))
    email = models.EmailField(_('Email'))

    class Meta:
        db_table = 'billing\'.\'customer'
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        indexes = [
            models.Index(
                fields=['user_id'],
                name='user_id_customer_idx'
            )
        ]

    def __str__(self):
        return str(self.email)
