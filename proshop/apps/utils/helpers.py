"""Helper utilities"""
import random
import string


def generate_order_number():
    """Generate unique order number"""
    timestamp = int(__import__('time').time() * 1000)
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ORD-{timestamp}-{random_suffix}"


def calculate_tax(amount, tax_rate=0.1):
    """Calculate tax on amount"""
    return round(amount * tax_rate, 2)


def format_currency(value):
    """Format value as currency string"""
    return f"${float(value):,.2f}"


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
