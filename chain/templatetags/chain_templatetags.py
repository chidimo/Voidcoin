from django import template

register = template.Library()

@register.filter()
def sum_amounts(list_of_transacton_objects):
    return sum([transaction['amount'] for transaction in list_of_transacton_objects])