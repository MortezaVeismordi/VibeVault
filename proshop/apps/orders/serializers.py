"""
Order API Serializers
"""
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    variant_sku = serializers.CharField(source='variant.sku', read_only=True)
    variant_name = serializers.SerializerMethodField(read_only=True)

    def get_variant_name(self, obj):
        if obj.variant:
            attributes = obj.variant.attributes or {}
            return f"{obj.variant.sku} - {attributes}"
        return obj.product.name

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_name',
            'variant_sku',
            'variant_name',
            'quantity',
            'unit_price',
            'total_price',
        ]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'user_name',
            'user_email',
            'status',
            'payment_status',
            'items',
            'subtotal',
            'shipping_cost',
            'tax',
            'total',
            'shipping_address',
            'shipping_city',
            'shipping_state',
            'shipping_postal_code',
            'shipping_country',
            'tracking_number',
            'estimated_delivery',
            'stripe_session_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'order_number',
            'status',
            'payment_status',
            'items',
            'subtotal',
            'shipping_cost',
            'tax',
            'total',
            'stripe_session_id',
            'tracking_number',
            'estimated_delivery',
            'created_at',
            'updated_at',
        ]
