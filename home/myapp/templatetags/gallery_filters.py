# myapp/templatetags/gallery_filters.py
from django import template

register = template.Library()

# Map từ tiếng Việt → class filter
SEASON_MAP = {
    'Xuân': 'xuan',
    'Hạ': 'ha',
    'Thu': 'thu',
    'Đông': 'dong',
}

@register.filter
def get_season_class(season_display):
    return f"filter-{SEASON_MAP.get(season_display, 'unknown')}"