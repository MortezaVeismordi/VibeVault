"""
Payment serializers for Stripe integration
"""
from rest_framework import serializers
from .models import Payment, PaymentLog, Refund


class PaymentLogSerializer(serializers.ModelSerializer):
    """Serializer for payment logs"""
    class Meta:
        model = PaymentLog
        fields = ['id', 'status', 'message', 'response_data', 'created_at']
        read_only_fields = ['id', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments"""
    logs = PaymentLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'amount',
            'currency',
            'payment_method',
            'status',
            'stripe_session_id',
            'stripe_payment_intent_id',
            'stripe_charge_id',
            'completed_at',
            'created_at',
            'updated_at',
            'logs',
        ]
        read_only_fields = [
            'id',
            'stripe_session_id',
            'stripe_payment_intent_id',
            'stripe_charge_id',
            'completed_at',
            'created_at',
            'updated_at',
        ]


class RefundSerializer(serializers.ModelSerializer):
    """Serializer for refunds"""
    class Meta:
        model = Refund
        fields = [
            'id',
            'payment',
            'amount',
            'reason',
            'status',
            'refund_transaction_id',
            'created_at',
            'processed_at',
        ]
        read_only_fields = [
            'id',
            'refund_transaction_id',
            'created_at',
            'processed_at',
        ]
