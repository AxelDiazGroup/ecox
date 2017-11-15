import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import COLORS
from expense.models import DebtLibrary, ExpenseLibrary


class DashboardView(View):
    template_name = "dashboard/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def get_context(self):
        context = {
            'parent_page_title': _('Dashboard'),
            'current_page_title': _('Economy'),
        }
        expense_list = []
        variables = {}
        expenses_data = []

        dates = (
            timezone.now() - relativedelta(months=1),
            timezone.now(),
            timezone.now() + relativedelta(months=1),
        )
        for date_filter in dates:
            expense = ExpenseLibrary(date_filter)
            debt = DebtLibrary(date_filter)
            expense_dict = dict(expense.get_dict(date_filter))
            import pdb; pdb.set_trace()
            debt_dict = dict(debt.get_dict(date_filter))
            variables.update(expense_dict)
            variables.update(debt_dict)

        context.update({'expenses_data': expenses_data})
        context.update({'colors_chart': COLORS})
        return context
