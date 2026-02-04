"""Signals for accounts app"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send welcome email to new users"""
    if created and instance.is_active:
        try:
            subject = 'Welcome to Proshop!'
            message = f'''
            Hi {instance.get_display_name()},
            
            Welcome to Proshop! We're excited to have you on board.
            
            You can now browse our products, add items to your cart, and place orders.
            
            Best regards,
            Proshop Team
            '''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending welcome email: {str(e)}")
