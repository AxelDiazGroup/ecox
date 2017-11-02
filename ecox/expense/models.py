from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import Account, Person


class Debt(Account):
    to = models.ForeignKey(Person, verbose_name=_('to'))
    pay_off = models.BooleanField(verbose_name=_('pay off'))

    def __str__(self):
        return "{}".format(self.to)


class Passage(Account):
    to = models.ForeignKey(Person, verbose_name=_('to'))

    def __str__(self):
        return "{}".format(self.to)


class Service(Account):

    def __str__(self):
        return "{}".format(self.description)


class Food(Account):

    def __str__(self):
        return "{}".format(self.description)


class Lease(Account):

    def __str__(self):
        return "{}".format(self.description)


class Family(Account):

    def __str__(self):
        return "{}".format(self.description)


class Expense(object):
    def __init__(self, created=timezone.now()):
        self.created = created
        self.debts = self.get_debt_balance()
        self.passages = self.get_passage_balance()
        self.services = self.get_services_balance()
        self.food = self.get_food_balance()
        self.lease = self.get_lease_balance()
        self.family = self.get_family_balance()

    def get_sum_balance(self, balance):
        if balance.exists():
            return float(balance.aggregate(Sum('balance'))['balance__sum'])
        else:
            return 0

    # Debt
    def get_negative_debts(self):
        return Debt.objects.filter(
            pay_off=False, created__month=self.created.month)

    def get_positive_debts(self):
        return Debt.objects.filter(
            pay_off=False, created__month=self.created.month)

    def get_positive_debts_balance(self):
        return self.get_sum_balance(self.get_positive_debts())

    def get_negative_debts_balance(self):
        return self.get_sum_balance(self.get_negative_debts())

    def get_debt_balance(self):
        return self.get_positive_debts_balance() - \
            self.get_negative_debts_balance()

    # Passage
    def get_passage(self):
        return Passage.objects.filter(created__month=self.created.month)

    def get_passage_balance(self):
        return self.get_sum_balance(self.get_passage())

    # Service
    def get_services(self):
        return Service.objects.filter(created__month=self.created.month)

    def get_services_balance(self):
        return self.get_sum_balance(self.get_services())

    # Foods
    def get_foods(self):
        return Food.objects.filter(created__month=self.created.month)

    def get_food_balance(self):
        return self.get_sum_balance(self.get_foods())

    # Lease
    def get_leases(self):
        return Lease.objects.filter(created__month=self.created.month)

    def get_lease_balance(self):
        return self.get_sum_balance(self.get_leases())

    # Family
    def get_family(self):
        return Family.objects.filter(created__month=self.created.month)

    def get_family_balance(self):
        return self.get_sum_balance(self.get_family())
