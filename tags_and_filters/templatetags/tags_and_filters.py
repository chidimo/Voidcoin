"""Custom template tags and filters"""
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
