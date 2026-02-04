"""
Admin configuration for Shop app.
Professional admin interface with inlines, search, filters, and preview.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q, Sum, Count
from .models import Category, Product, ProductVariant, ProductImage


# ===========================
# CATEGORY ADMIN
# ===========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for product categories with hierarchical support."""
    list_display = ('name_with_icon', 'slug', 'parent', 'product_count', 'is_active', 'ordering')
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering_fields = ['ordering', 'name']
    list_editable = ('is_active', 'ordering')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'parent')
        }),
        ('Content', {
            'fields': ('description', 'icon')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'ordering')
        }),
    )

    def name_with_icon(self, obj):
        """Display category name with icon."""
        if obj.icon:
            return format_html(f'<i class="{obj.icon}"></i> {obj.name}')
        return obj.name
    name_with_icon.short_description = 'Category'

    def product_count(self, obj):
        """Display count of products in this category."""
        count = obj.products.filter(is_active=True).count()
        return format_html(f'<strong>{count}</strong>')
    product_count.short_description = 'Products'


# ===========================
# PRODUCT VARIANT INLINE
# ===========================

class ProductVariantInline(admin.TabularInline):
    """Inline admin for product variants."""
    model = ProductVariant
    extra = 1
    fields = ('sku', 'attributes', 'price', 'cost_price', 'stock', 'is_default', 'is_active', 'ordering')
    ordering_fields = ['ordering']
    list_display_links = ['sku']

    def get_queryset(self, request):
        """Optimize queries."""
        qs = super().get_queryset(request)
        return qs.select_related('product')


# ===========================
# PRODUCT IMAGE INLINE
# ===========================

class ProductImageInline(admin.TabularInline):
    """Inline admin for product images with preview."""
    model = ProductImage
    extra = 1
    fields = ('image_preview', 'image', 'variant', 'alt_text', 'is_primary', 'ordering')
    readonly_fields = ('image_preview',)
    ordering_fields = ['ordering']

    def image_preview(self, obj):
        """Display image thumbnail preview."""
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />'
            )
        return "No image"
    image_preview.short_description = 'Preview'


# ===========================
# PRODUCT ADMIN
# ===========================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Professional admin for products with inlines and powerful search."""
    list_display = (
        'name_with_image',
        'sku',
        'category',
        'price_display',
        'stock_display',
        'is_featured',
        'is_active',
    )
    list_filter = (
        'is_active',
        'is_featured',
        'is_bestseller',
        'is_new',
        'category',
        'brand',
        ('created_at', admin.DateFieldListFilter),
    )
    search_fields = (
        'name',
        'sku',
        'brand',
        'description',
        'meta_keywords',
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'stock_status_display')
    inlines = [ProductVariantInline, ProductImageInline]
    date_hierarchy = 'created_at'
    actions = ['mark_featured', 'unmark_featured', 'mark_bestseller', 'unmark_bestseller']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand'),
            'description': 'Product identification and categorization',
        }),
        ('Description & Content', {
            'fields': ('description', 'short_description'),
        }),
        ('Pricing & Inventory', {
            'fields': (
                'base_price',
                'cost_price',
                'stock',
                'stock_status_display',
            ),
            'description': 'Price and stock info (overridden by variants if they exist)',
        }),
        ('Status & Visibility', {
            'fields': (
                'is_active',
                'is_featured',
                'is_bestseller',
                'is_new',
            ),
            'classes': ('collapse',),
        }),
        ('SEO & Marketing', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
            ),
            'classes': ('collapse',),
        }),
        ('Ratings', {
            'fields': ('rating', 'review_count'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        """Optimize queries with annotations."""
        qs = super().get_queryset(request)
        qs = qs.select_related('category')
        qs = qs.prefetch_related('variants', 'images')
        qs = qs.annotate(
            variant_count=Count('variants'),
            image_count=Count('images'),
        )
        return qs

    def name_with_image(self, obj):
        """Display product name with thumbnail."""
        image = obj.get_primary_image()
        if image and image.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover; margin-right: 10px;" />'
                '<strong>{}</strong>',
                image.image.url,
                obj.name,
            )
        return f'<strong>{obj.name}</strong>'
    name_with_image.short_description = 'Product'

    def price_display(self, obj):
        """Display product price with color coding."""
        price = obj.get_price()
        if price:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">${:.2f}</span>',
                price,
            )
        return '-'
    price_display.short_description = 'Price'

    def stock_display(self, obj):
        """Display stock with color coding (red if low)."""
        stock = obj.get_available_stock()
        if stock > 10:
            color = '#28a745'  # Green
        elif stock > 0:
            color = '#ffc107'  # Yellow
        else:
            color = '#dc3545'  # Red
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            stock,
        )
    stock_display.short_description = 'Stock'

    def stock_status_display(self, obj):
        """Display detailed stock status."""
        stock = obj.get_available_stock()
        variants = obj.variants.count()
        
        if variants > 0:
            status = f"Has {variants} variants with total stock: {stock}"
        else:
            status = f"Base stock: {stock}"
        
        return status
    stock_status_display.short_description = 'Stock Status'

    # Admin actions
    def mark_featured(self, request, queryset):
        """Mark selected products as featured."""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} products marked as featured.')
    mark_featured.short_description = 'Mark selected as featured'

    def unmark_featured(self, request, queryset):
        """Unmark selected products as featured."""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} products unmarked as featured.')
    unmark_featured.short_description = 'Unmark selected as featured'

    def mark_bestseller(self, request, queryset):
        """Mark selected products as bestsellers."""
        count = queryset.update(is_bestseller=True)
        self.message_user(request, f'{count} products marked as bestsellers.')
    mark_bestseller.short_description = 'Mark selected as bestsellers'

    def unmark_bestseller(self, request, queryset):
        """Unmark selected products as bestsellers."""
        count = queryset.update(is_bestseller=False)
        self.message_user(request, f'{count} products unmarked as bestsellers.')
    unmark_bestseller.short_description = 'Unmark selected as bestsellers'


# ===========================
# PRODUCT VARIANT ADMIN
# ===========================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin for managing variants independently."""
    list_display = ('sku', 'product', 'attributes_display', 'price', 'stock', 'is_default', 'is_active')
    list_filter = ('is_active', 'is_default', 'product__category', ('created_at', admin.DateFieldListFilter))
    search_fields = ('sku', 'product__name', 'product__sku')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Product & Variant Info', {
            'fields': ('product', 'sku')
        }),
        ('Attributes', {
            'fields': ('attributes',),
            'description': 'JSON format: {"size": "XL", "color": "Red"}',
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'cost_price', 'stock', 'markup_percentage')
        }),
        ('Status', {
            'fields': ('is_default', 'is_active', 'ordering')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        """Optimize queries."""
        return super().get_queryset(request).select_related('product')

    def attributes_display(self, obj):
        """Display attributes in readable format."""
        if obj.attributes:
            attrs = ', '.join([f'{k}: {v}' for k, v in obj.attributes.items()])
            return attrs
        return '-'
    attributes_display.short_description = 'Attributes'

    def markup_percentage(self, obj):
        """Display markup as readonly."""
        return f'{obj.markup_percentage:.1f}%'
    markup_percentage.short_description = 'Markup %'


# ===========================
# PRODUCT IMAGE ADMIN
# ===========================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin for managing product images."""
    list_display = ('image_thumbnail', 'product', 'variant', 'alt_text', 'is_primary', 'ordering')
    list_filter = ('is_primary', 'product__category', ('created_at', admin.DateFieldListFilter))
    search_fields = ('product__name', 'alt_text', 'product__sku')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    list_editable = ('is_primary', 'ordering')
    
    fieldsets = (
        ('Image Assignment', {
            'fields': ('product', 'variant')
        }),
        ('Image & Alt Text', {
            'fields': ('image', 'image_preview', 'alt_text')
        }),
        ('Display', {
            'fields': ('is_primary', 'ordering')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        """Optimize queries."""
        return super().get_queryset(request).select_related('product', 'variant')

    def image_thumbnail(self, obj):
        """Display image thumbnail in list."""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url,
            )
        return 'No image'
    image_thumbnail.short_description = 'Image'

    def image_preview(self, obj):
        """Display large image preview in detail view."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url,
            )
        return 'No image'
    image_preview.short_description = 'Preview'

