# myapp/templatetags/price_filters.py
from django import template
import locale

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    if value is None:
        return "0đ"
    try:
        # Định dạng số có dấu chấm ngăn cách
        return f"{int(value):,}".replace(",", ".") + "đ"
    except (ValueError, TypeError):
        return "0đ"