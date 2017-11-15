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
        item_chart = {}
        expenses_data = []

        dates = (
            timezone.now() - relativedelta(months=1),
            timezone.now(),
            timezone.now() + relativedelta(months=1),
        )
        for date_filter in dates:
            expense = Expense(date_filter)

            variables = expense.get_dict(date_filter)

            for key, value in list(expense.__dict__.items()):
                if isinstance(value, (datetime, date)):
                    value = value.isoformat()
                item_chart = {'name': key, 'value': value}
                expense_list.append(dict(item_chart))
            variables.update({'expenses': json.dumps(expense_list)})
            expenses_data.append(variables)

        context.update({'expenses_data': expenses_data})
        context.update({'colors_chart': COLORS})
        return context
