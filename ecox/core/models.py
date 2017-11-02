from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from djmoney.models.fields import MoneyField

from model_utils.models import TimeStampedModel, TimeFramedModel

COLORS = [
    '#00c292',
    '#01c0c8',
    '#fb9678',
    '#fec107',
    '#6e4ac3',
    '#55c4c9',
]


class Account(TimeStampedModel, TimeFramedModel):
    balance = MoneyField(max_digits=10, decimal_places=2,
                         default_currency='CLP', verbose_name=_('amount'))
    description = models.TextField(verbose_name=_('description'))

    class Meta:
        abstract = True


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    lastname = models.CharField(blank=True, max_length=100,
                                verbose_name=_('lastname'))
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: "
                  "'+999999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=15, blank=True)

    def __str__(self):
        return "{}".format(self.name)
