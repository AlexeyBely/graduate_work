from django.db import models
from django.utils.translation import gettext_lazy as _


MAX_LENGTH_NAME = 255


class IdMixin(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class Tariff(IdMixin):
    """Describes the tariff for a privileged role."""
    role = models.CharField(_('Role'), max_length=MAX_LENGTH_NAME)
    description = models.TextField(_('Description'), blank=True, null=True)
    price = models.FloatField(_('Price'))
    auth_role_id = models.UUIDField(_('ID_auth_role'), unique=True, 
                                    blank=True, null=True)

    class Meta:
        db_table = 'marketing\".\"tariff'
        verbose_name = _('tariff')
        verbose_name_plural = _('tariffs')

    def __str__(self):
        return self.role
    

class PersonalDiscount(IdMixin):
    """Personal discount for the user."""
    user_id = models.UUIDField(_('ID_user'), unique=True)
    discount = models.IntegerField(_('Discount'))

    class Meta:
        db_table = 'marketing\".\"personal_discount'
        verbose_name = _('personal_discount')
        verbose_name_plural = _('personal_discounts')
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', ],
                name='personal_discount_unique'
            ),
        ]

    def __str__(self):
        return str(self.discount)
    

class MonthsDiscount(IdMixin):
    """Discount on the number of months purchased."""
    amount_months = models.IntegerField(_('Months'))
    discount = models.IntegerField(_('Discount'))

    class Meta:
        db_table = 'marketing\".\"months_discount'
        verbose_name = _('months_discount')
        verbose_name_plural = _('months_discounts')

    def __str__(self):
        return str(self.discount)
    

class Promocode(IdMixin):
    """Promotion with certain parameters."""
    code = models.CharField(_('Promocode'), max_length=MAX_LENGTH_NAME)
    description = models.TextField(_('Description'), blank=True, null=True)
    role = models.CharField(_('Role'), max_length=MAX_LENGTH_NAME)
    discount = models.IntegerField(_('Discount'))
    amount_months = models.IntegerField(_('Months'))
    expiration = models.DateTimeField(_('Expiration'))

    class Meta:
        db_table = 'marketing\".\"promocode'
        verbose_name = _('promocode')
        verbose_name_plural = _('promocodes')

    def __str__(self):
        return self.code
