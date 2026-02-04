"""
Shop application models - Products, Categories, Variants, Images
Professional e-commerce models with best practices for 2025-2026.
"""
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.conf import settings


# ===========================
# ABSTRACT MODELS
# ===========================

class TimestampedModel(models.Model):
    """
    Abstract model that adds created_at and updated_at timestamps.
    Use this for all models that need timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


# ===========================
# CATEGORY MODEL
# ===========================

class Category(TimestampedModel):
    """
    Product category with support for hierarchical structure (parent-child).
    Uses self-referencing ForeignKey for flexibility and simplicity.
    """
    name = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Category name (e.g., 'Electronics', 'Smartphones')"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="URL-friendly name (auto-generated from name)"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed category description"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class (e.g., 'fas fa-mobile-alt')"
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
        help_text="Parent category (leave empty for top-level categories)"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this category is visible in the store"
    )
    ordering = models.PositiveSmallIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['ordering', 'name']
        unique_together = [['slug', 'parent']]
        indexes = [
            models.Index(fields=['is_active', 'ordering']),
            models.Index(fields=['parent', 'is_active']),
        ]

    def __str__(self):
        """Return category name with parent hierarchy."""
        if self.parent:
            return f"{self.parent} → {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return category URL."""
        return f"/shop/category/{self.slug}/"

    @property
    def product_count(self):
        """Get total products in this category and subcategories."""
        count = self.products.filter(is_active=True).count()
        for child in self.children.all():
            count += child.product_count
        return count


# ===========================
# PRODUCT MODEL - CUSTOM QUERYSET & MANAGER
# ===========================

class ProductQuerySet(models.QuerySet):
    """Custom QuerySet for Product with common filters."""

    def active(self):
        """Get only active products."""
        return self.filter(is_active=True)

    def featured(self):
        """Get only featured products."""
        return self.filter(is_featured=True, is_active=True)

    def bestsellers(self):
        """Get only bestseller products."""
        return self.filter(is_bestseller=True, is_active=True)


class ProductManager(models.Manager):
    """Custom manager for Product with optimized queries."""

    def get_queryset(self):
        """Optimize queries with select_related."""
        return ProductQuerySet(self.model, using=self._db).select_related('category')

    def active(self):
        """Get only active products."""
        return self.get_queryset().active()

    def featured(self):
        """Get only featured products."""
        return self.get_queryset().featured()

    def bestsellers(self):
        """Get only bestseller products."""
        return self.get_queryset().bestsellers()


# ===========================
# PRODUCT MODEL
# ===========================

class Product(TimestampedModel):
    """
    Main product model supporting variants (size, color, etc.).
    If product has variants, price and stock come from variants.
    If product has no variants, price and stock are used directly.
    """
    # Use custom manager
    objects = ProductManager()
    
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Product name"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="URL-friendly product name"
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Stock Keeping Unit (required if no variants)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        help_text="Product category"
    )
    brand = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Product brand/manufacturer"
    )
    description = models.TextField(
        help_text="Full product description (supports HTML)"
    )
    short_description = models.CharField(
        max_length=500,
        blank=True,
        help_text="Brief one-line description for listings"
    )
    
    # Pricing & Inventory (used when no variants exist)
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Base price (used if no variants)"
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Cost price for profit calculations"
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Total stock (aggregated from variants if they exist)"
    )
    
    # Status flags
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether product is available for sale"
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether to feature on homepage"
    )
    is_bestseller = models.BooleanField(
        default=False,
        help_text="Whether product is a bestseller"
    )
    is_new = models.BooleanField(
        default=False,
        help_text="Whether product is newly added"
    )
    
    # SEO & Metadata
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="SEO title (leave empty to use name)"
    )
    meta_description = models.CharField(
        max_length=500,
        blank=True,
        help_text="SEO meta description"
    )
    meta_keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="SEO keywords (comma-separated)"
    )
    
    # Ratings & Reviews (for future use)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Average rating (0-5)"
    )
    review_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of reviews"
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'category']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['brand', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        """Return product name with SKU."""
        sku = self.sku or "no SKU"
        return f"{self.name} ({sku})"

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return product URL."""
        return f"/shop/product/{self.slug}/"

    def get_price(self):
        """
        Get product price.
        If variants exist, return minimum variant price.
        Otherwise, return base price.
        """
        if self.variants.exists():
            min_price = self.variants.aggregate(
                min_price=models.Min('price')
            )['min_price']
            return min_price or self.base_price
        return self.base_price

    def get_available_stock(self):
        """
        Get available stock.
        If variants exist, sum all variant stocks.
        Otherwise, return product stock.
        """
        if self.variants.exists():
            total_stock = self.variants.aggregate(
                total=models.Sum('stock')
            )['total'] or 0
            return total_stock
        return self.stock

    def is_in_stock(self):
        """Check if product has available stock."""
        return self.get_available_stock() > 0

    def get_primary_image(self):
        """Get primary/featured product image."""
        return self.images.filter(is_primary=True).first() or self.images.first()


# ===========================
# PRODUCT VARIANT MODEL
# ===========================

class ProductVariant(TimestampedModel):
    """
    Product variant for different sizes, colors, configurations, etc.
    Each variant has its own SKU, price, and stock.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        help_text="Parent product"
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Variant-specific SKU"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Variant price"
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Variant cost price"
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Available stock for this variant"
    )
    
    # Attributes as JSON (e.g., {"size": "XL", "color": "Red"})
    attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text='Variant attributes (e.g., {"size": "XL", "color": "Red"})'
    )
    
    # Display options
    is_default = models.BooleanField(
        default=False,
        help_text="Set as default variant for product"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this variant is available"
    )
    ordering = models.PositiveSmallIntegerField(
        default=0,
        help_text="Display order"
    )

    class Meta:
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        ordering = ['ordering', 'sku']
        unique_together = [['product', 'sku']]
        indexes = [
            models.Index(fields=['product', 'is_active']),
            models.Index(fields=['is_default', 'product']),
        ]

    def __str__(self):
        """Return variant display name."""
        attrs = " | ".join([f"{k}: {v}" for k, v in self.attributes.items()])
        return f"{self.product.name} - {attrs}" if attrs else f"{self.product.name} ({self.sku})"

    def save(self, *args, **kwargs):
        """Ensure only one default variant per product."""
        if self.is_default:
            ProductVariant.objects.filter(product=self.product, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def is_in_stock(self):
        """Check if variant has available stock."""
        return self.stock > 0

    @property
    def markup_percentage(self):
        """Calculate markup percentage (for inventory management)."""
        if self.cost_price and self.cost_price > 0:
            return ((self.price - self.cost_price) / self.cost_price) * 100
        return 0


# ===========================
# PRODUCT IMAGE MODEL
# ===========================

class ProductImage(TimestampedModel):
    """
    Product images with support for variant-specific images.
    Can attach images to product (all variants) or specific variant.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Product (required)"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images',
        help_text="Specific variant (optional - leave empty for all variants)"
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        help_text="Product image"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alt text for accessibility and SEO"
    )
    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Set as primary/featured image"
    )
    ordering = models.PositiveSmallIntegerField(
        default=0,
        help_text="Display order"
    )

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['ordering']
        unique_together = [['product', 'image']]
        indexes = [
            models.Index(fields=['product', 'is_primary']),
            models.Index(fields=['product', 'variant']),
        ]

    def __str__(self):
        """Return image identifier."""
        variant_info = f" - {self.variant}" if self.variant else ""
        return f"{self.product.name}{variant_info}"

    def save(self, *args, **kwargs):
        """Ensure only one primary image per product-variant combination."""
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product,
                variant=self.variant,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


# EOF


