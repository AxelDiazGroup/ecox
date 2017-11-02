from django import template

register = template.Library()


@register.filter(name='percent')
def percent(value, total):
    if total == 0:
        return 0
    if not value or value == '':
        value = 0
    percent = (value * 100) / total
    return "%.2f" % percent
