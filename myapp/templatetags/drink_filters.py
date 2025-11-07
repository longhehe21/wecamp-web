# your_app/templatetags/menu_filters.py
from django import template
register = template.Library()

@register.filter
def filter_by_type(items, drink_type):
    return items.filter(drink_type=drink_type)