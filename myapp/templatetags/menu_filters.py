# your_app/templatetags/menu_filters.py
from django import template
register = template.Library()

@register.filter
def filter_by_type(items, meal_type):
    return items.filter(meal_type=meal_type)