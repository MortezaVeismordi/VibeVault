"""
Shop API Serializers
Professional product serializers with nested relationships and optimization.
"""
from rest_framework import serializers
from apps.shop.models import Category, Product, ProductVariant, ProductImage


# ===========================
# PRODUCT IMAGE SERIALIZER
# ===========================

class ProductImageSerializer(serializers.ModelSerializer):
    """Simple serializer for product images."""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'ordering']
        read_only_fields = ['id', 'created_at', 'updated_at']


# ===========================
# PRODUCT VARIANT SERIALIZER
# ===========================

class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for product variants with nested images."""
    
    images = ProductImageSerializer(many=True, read_only=True)
    markup_percentage = serializers.SerializerMethodField(read_only=True)
    is_in_stock = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'sku', 'price', 'cost_price', 'stock', 
            'attributes', 'is_default', 'is_active', 'ordering',
            'images', 'markup_percentage', 'is_in_stock',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_markup_percentage(self, obj):
        """Return markup percentage."""
        return obj.markup_percentage
    
    def get_is_in_stock(self, obj):
        """Return stock availability."""
        return obj.is_in_stock()


# ===========================
# CATEGORY SERIALIZER
# ===========================

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""
    
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon',
            'parent', 'is_active', 'ordering', 'product_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'product_count']
    
    def get_product_count(self, obj):
        """Return the count of active products in this category."""
        return obj.product_count


# ===========================
# PRODUCT LIST SERIALIZER
# ===========================

class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listing."""
    
    category = serializers.StringRelatedField(read_only=True)
    primary_image = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    available_stock = serializers.SerializerMethodField(read_only=True)
    is_available = serializers.SerializerMethodField(read_only=True)
    rating_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'brand', 'category',
            'short_description', 'price', 'available_stock', 'is_available',
            'is_featured', 'is_bestseller', 'is_new', 'rating_display',
            'primary_image', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_primary_image(self, obj):
        """Return primary product image URL."""
        image = obj.get_primary_image()
        if image and image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
        return None
    
    def get_price(self, obj):
        """Return product price (min variant or base)."""
        price = obj.get_price()
        return str(price) if price else None
    
    def get_available_stock(self, obj):
        """Return available stock."""
        return obj.get_available_stock()
    
    def get_is_available(self, obj):
        """Return stock availability."""
        return obj.is_in_stock()
    
    def get_rating_display(self, obj):
        """Return rating with review count."""
        if obj.rating and obj.rating > 0:
            return f"{obj.rating}/5.0 ({obj.review_count} reviews)"
        return "Not rated"


# ===========================
# PRODUCT DETAIL SERIALIZER
# ===========================

class ProductDetailSerializer(serializers.ModelSerializer):
    """Full product serializer with nested relationships."""
    
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    available_stock = serializers.SerializerMethodField(read_only=True)
    is_available = serializers.SerializerMethodField(read_only=True)
    rating_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'brand', 'category',
            'description', 'short_description', 
            'base_price', 'cost_price', 'price',
            'stock', 'available_stock', 'is_available',
            'is_active', 'is_featured', 'is_bestseller', 'is_new',
            'meta_title', 'meta_description', 'meta_keywords',
            'rating', 'review_count', 'rating_display',
            'primary_image', 'images', 'variants',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_primary_image(self, obj):
        """Return primary product image URL."""
        image = obj.get_primary_image()
        if image and image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
        return None
    
    def get_price(self, obj):
        """Return product price (min variant or base)."""
        price = obj.get_price()
        return str(price) if price else None
    
    def get_available_stock(self, obj):
        """Return available stock (variant sum or base)."""
        return obj.get_available_stock()
    
    def get_is_available(self, obj):
        """Return stock availability."""
        return obj.is_in_stock()
    
    def get_rating_display(self, obj):
        """Return rating with review count."""
        if obj.rating and obj.rating > 0:
            return f"{obj.rating}/5.0 ({obj.review_count} reviews)"
        return "Not rated"
