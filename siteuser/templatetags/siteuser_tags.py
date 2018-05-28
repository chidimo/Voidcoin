from django import template

register = template.Library()

@register.filter()
def remove_at_from_email(email_address):
    return email_address.split('@')[0]

@register.filter()
def count_published(queryset):
    return queryset.filter(publish=True).count()
