import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import COLORS
from expense.models import Debt, Expense


class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def get_context(self):
        context = {
            'parent_page_title': _('Dashboard'),
            'current_page_title': _('Economy'),
        }
        expense_list = []
        item_chart = {}
        expenses_data = []

        dates = (
            timezone.now() - relativedelta(months=1),
            timezone.now(),
            timezone.now() + relativedelta(months=1),
        )
        for date_filter in dates:
            expense = Expense(date_filter)

            # Debts
            positive_debts_balance = expense.get_positive_debts_balance()
            negative_debts_balance = expense.get_negative_debts_balance()
            debts_balance = expense.debts
            # Passage
            passage_balance = expense.passages
            # Services
            service_balance = expense.services
            # Food
            food_balance = expense.food
            # Lease
            lease_balance = expense.lease
            # Family
            family_balance = expense.family
            total_expense = \
                negative_debts_balance + \
                passage_balance + \
                service_balance + \
                food_balance + \
                lease_balance

            for key, value in list(expense.__dict__.items()):
                if isinstance(value, (datetime, date)):
                    value = value.isoformat()
                item_chart = {'name': key, 'value': value}
                expense_list.append(dict(item_chart))
            expenses = json.dumps(expense_list)
            balance = positive_debts_balance - negative_debts_balance

            variables = {}
            variables.update({'negative_debts_balance': negative_debts_balance})
            variables.update({'positive_debts_balance': positive_debts_balance})

            variables.update({'debts_balance': debts_balance})
            variables.update({'passage_balance': passage_balance})
            variables.update({'service_balance': service_balance})
            variables.update({'food_balance': food_balance})
            variables.update({'lease_balance': lease_balance})
            variables.update({'family_balance': family_balance})
            variables.update({'total_expense': total_expense})
            variables.update({'expenses': expenses})
            variables.update({'date': date_filter})
            variables.update({'moment': 'current'})
            if date_filter.month < timezone.now().month:
                variables.update({'moment': 'past'})
            elif date_filter.month > timezone.now().month:
                variables.update({'moment': 'future'})

            expenses_data.append(variables)
        context.update({'expenses_data': expenses_data})
        context.update({'colors_chart': COLORS})
        return context
