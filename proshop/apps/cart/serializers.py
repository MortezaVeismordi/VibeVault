"""
Cart Serializers for DRF API endpoints
"""
from rest_framework import serializers
from .models import Cart, CartItem
from apps.shop.serializers import ProductVariantSerializer
from apps.shop.models import ProductVariant


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for cart items with nested variant details.
    """
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        write_only=True,
        source='variant'
    )
    product_name = serializers.CharField(
        source='variant.product.name',
        read_only=True
    )
    product_sku = serializers.CharField(
        source='variant.sku',
        read_only=True
    )
    subtotal = serializers.SerializerMethodField(read_only=True)
    is_in_stock = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'variant', 'variant_id', 'product_name', 'product_sku',
            'quantity', 'price_at_add', 'subtotal', 'is_in_stock',
            'added_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'variant', 'price_at_add', 'added_at', 'updated_at'
        ]
    
    def get_subtotal(self, obj):
        """Return subtotal for this item"""
        return float(obj.get_subtotal())
    
    def get_is_in_stock(self, obj):
        """Check if quantity is in stock"""
        return obj.is_in_stock()
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for shopping cart with nested items.
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    has_items = serializers.BooleanField(read_only=True)
    user_id = serializers.IntegerField(
        source='user.id',
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user_id', 'total_items', 'total_price', 'has_items',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """
    Serializer for adding items to cart.
    """
    variant_id = serializers.IntegerField(
        help_text="ProductVariant ID to add"
    )
    quantity = serializers.IntegerField(
        default=1,
        min_value=1,
        help_text="Quantity to add"
    )
    
    def validate_variant_id(self, value):
        """Validate variant exists"""
        try:
            ProductVariant.objects.get(id=value, is_active=True)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError("Variant not found or inactive")
        return value
    
    def validate(self, attrs):
        """Validate quantity against stock"""
        variant_id = attrs.get('variant_id')
        quantity = attrs.get('quantity')
        
        try:
            variant = ProductVariant.objects.get(id=variant_id)
            if quantity > variant.stock:
                raise serializers.ValidationError(
                    f"Requested quantity ({quantity}) exceeds available stock ({variant.stock})"
                )
        except ProductVariant.DoesNotExist:
            pass
        
        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    """
    Serializer for updating cart item quantity.
    """
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="New quantity"
    )
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value


class CheckoutSessionSerializer(serializers.Serializer):
    """
    Serializer for checkout session creation.
    """
    session_id = serializers.CharField(read_only=True)
    checkout_url = serializers.CharField(read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    items_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        fields = ['session_id', 'checkout_url', 'total_amount', 'items_count']
