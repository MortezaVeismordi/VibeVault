"""
Order signals for email notifications and other events
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order


@receiver(post_save, sender=Order)
def send_order_notification_email(sender, instance, created, **kwargs):
    """
    Send email when order is created or status changes
    """
    if created:
        # Order created - send confirmation
        send_order_confirmation_email(instance)
    elif instance.payment_status == 'paid':
        # Payment completed
        send_order_paid_email(instance)
    elif instance.status == 'shipped':
        # Order shipped
        send_order_shipped_email(instance)


def send_order_confirmation_email(order):
    """Send order confirmation email"""
    try:
        subject = f"Order Confirmation - {order.order_number}"
        
        items_list = "\n".join([
            f"- {item.product.name} (x{item.quantity}): ${item.total_price}"
            for item in order.items.all()
        ])
        
        message = f"""
Dear {order.user.get_full_name() or order.user.email},

Thank you for your order!

Order Number: {order.order_number}
Order Date: {order.created_at.strftime('%B %d, %Y')}

Items:
{items_list}

Subtotal: ${order.subtotal}
Shipping: ${order.shipping_cost}
Tax: ${order.tax}
Total: ${order.total}

Shipping Address:
{order.shipping_address}
{order.shipping_city}, {order.shipping_state} {order.shipping_postal_code}
{order.shipping_country}

Your order is pending payment. Please complete payment to proceed.

Best regards,
Proshop Team
noreply@proshop.com
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending order confirmation email: {str(e)}")


def send_order_paid_email(order):
    """Send payment confirmation email"""
    try:
        subject = f"Payment Confirmed - {order.order_number}"
        
        message = f"""
Dear {order.user.get_full_name() or order.user.email},

Your payment has been received and confirmed!

Order Number: {order.order_number}
Total Paid: ${order.total}
Payment Status: Paid

Your order is now being processed. You will receive tracking information soon.

Best regards,
Proshop Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending payment email: {str(e)}")


def send_order_shipped_email(order):
    """Send shipping notification email"""
    try:
        subject = f"Order Shipped - {order.order_number}"
        
        message = f"""
Dear {order.user.get_full_name() or order.user.email},

Your order has been shipped!

Order Number: {order.order_number}
Tracking Number: {order.tracking_number or 'N/A'}
Estimated Delivery: {order.estimated_delivery.strftime('%B %d, %Y') if order.estimated_delivery else 'TBD'}

Best regards,
Proshop Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending shipping email: {str(e)}")
