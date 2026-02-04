from django.db import models
from django.utils import timezone
from apps.orders.models import Order


class Payment(models.Model):
    """Payment transactions with Stripe integration"""
    PAYMENT_METHOD = [
        ('stripe', 'Stripe'),
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='stripe')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    # Stripe IDs
    stripe_session_id = models.CharField(max_length=200, blank=True, null=True, unique=True, db_index=True)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    stripe_charge_id = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    # Legacy fields
    transaction_id = models.CharField(max_length=200, unique=True, blank=True, null=True)
    payment_token = models.CharField(max_length=500, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stripe_session_id']),
            models.Index(fields=['stripe_payment_intent_id']),
            models.Index(fields=['stripe_charge_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Payment for {self.order.order_number} ({self.status})"

    def mark_succeeded(self, stripe_charge_id=None):
        """Mark payment as succeeded"""
        self.status = 'succeeded'
        self.completed_at = timezone.now()
        if stripe_charge_id:
            self.stripe_charge_id = stripe_charge_id
        self.save()

    def mark_failed(self):
        """Mark payment as failed"""
        self.status = 'failed'
        self.save()


class PaymentLog(models.Model):
    """Log of payment attempts and status changes"""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=20)
    message = models.TextField()
    response_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Log for {self.payment.order.order_number}"


class Refund(models.Model):
    """Refund records"""
    REFUND_STATUS = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS, default='requested')
    refund_transaction_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Refund for {self.payment.order.order_number}"
