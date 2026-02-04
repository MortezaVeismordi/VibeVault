"""Custom template filters"""
from django import template

register = template.Library()


@register.filter
def currency(value):
    """Format value as currency"""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return value


@register.filter
def discount_percentage(price, discount_price):
    """Calculate discount percentage"""
    try:
        return round(((float(price) - float(discount_price)) / float(price)) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def truncate_words(value, num_words=20):
    """Truncate text to N words"""
    words = value.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return value
