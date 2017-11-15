from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import Account, Person, Moment, Balance


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


class DebtLibrary(Moment, Balance):
    def __init__(self, start=timezone.now()):
        self.start = start

    def get_debts(self):
        return self.get_debt_balance()

    def get_negative_debts(self):
        return Debt.objects.filter(
            pay_off=False, start__month=self.start.month)

    def get_positive_debts(self):
        return Debt.objects.filter(
            pay_off=False, start__month=self.start.month)

    def get_positive_debts_balance(self):
        return self.get_sum_balance(self.get_positive_debts())

    def get_negative_debts_balance(self):
        return self.get_sum_balance(self.get_negative_debts())

    def get_debt_balance(self):
        return self.get_positive_debts_balance() - \
            self.get_negative_debts_balance()

    def get_dict(self, date_filter):
        debt = {'amount': 0, 'description': ''}
        debts = Debt.objects.filter(start__month=self.start.month)
        if not debts.exists():
            return debt
        else:
            return debt.values()
        return debts


class ExpenseLibrary(DebtLibrary, Balance):
    def __init__(self, start=timezone.now()):
        self.start = start
        self.food = self.get_food_balance()
        self.lease = self.get_lease_balance()
        self.passages = self.get_passage_balance()
        self.services = self.get_services_balance()
        self.family = self.get_family_balance()

    # Passage
    def get_passage(self):
        return Passage.objects.filter(start__month=self.start.month)

    def get_passage_balance(self):
        return self.get_sum_balance(self.get_passage())

    # Service
    def get_services(self):
        return Service.objects.filter(start__month=self.start.month)

    def get_services_balance(self):
        return self.get_sum_balance(self.get_services())

    # Foods
    def get_foods(self):
        return Food.objects.filter(start__month=self.start.month)

    def get_food_balance(self):
        return self.get_sum_balance(self.get_foods())

    # Lease
    def get_leases(self):
        return Lease.objects.filter(start__month=self.start.month)

    def get_lease_balance(self):
        return self.get_sum_balance(self.get_leases())

    # Family
    def get_family(self):
        return Family.objects.filter(start__month=self.start.month)

    def get_family_balance(self):
        return self.get_sum_balance(self.get_family())

    def get_dict(self, date_filter):
        variables = self.get_variables(date_filter)
        total_expense = \
            self.get_negative_debts_balance() + \
            self.passages + \
            self.services + \
            self.food + \
            self.family

        variables.update(
            {'negative_debts_balance': self.get_negative_debts_balance()})
        variables.update(
            {'positive_debts_balance': self.get_positive_debts_balance()})
        variables.update({'debts_balance': self.get_debts()})
        variables.update({'passage_balance': self.passages})
        variables.update({'service_balance': self.services})
        variables.update({'food_balance': self.food})
        variables.update({'lease_balance': self.lease})
        variables.update({'family_balance': self.family})
        variables.update({'total_expense': total_expense})
        return variables
