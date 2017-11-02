from django.contrib import admin
from .models import Passage, Debt, Service, Food, Lease, Family


class DebtAdmin(admin.ModelAdmin):
    list_display = ['to', 'balance', 'description', 'pay_off']


admin.site.register(Passage)
admin.site.register(Service)
admin.site.register(Food)
admin.site.register(Lease)
admin.site.register(Family)
admin.site.register(Debt, DebtAdmin)
