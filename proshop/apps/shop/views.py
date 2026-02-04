"""
Shop views and API endpoints
"""
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category, ProductVariant, ProductImage
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductVariantSerializer,
    ProductImageSerializer,
)


# ===========================
# TRADITIONAL VIEWS
# ===========================

def shop_list(request):
    """Display all products with filtering and search"""
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query)
        )

    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)

    context = {
        'products': products,
        'categories': categories,
        'query': query,
    }
    return render(request, 'shop/shop.html', context)


def product_detail(request, slug):
    """Display product details"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


def category_detail(request, slug):
    """Display all products in a category"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category.html', context)


# ===========================
# API VIEWSETS
# ===========================

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for product categories.
    
    Supports:
    - Listing all categories
    - Filtering by parent
    - Searching by name
    - Ordering by name, ordering
    """
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'ordering']
    ordering = ['ordering', 'name']
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get products in this category."""
        category = self.get_object()
        products = Product.objects.filter(
            category=category,
            is_active=True
        ).select_related('category').prefetch_related(
            'variants', 'images'
        )
        serializer = ProductListSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for products.
    
    Supports:
    - Listing all products (paginated, 20 per page)
    - Filtering by category, featured, bestseller, stock status
    - Searching by name, brand, description
    - Ordering by name, price, rating, created date
    - Price range filtering via min_price/max_price
    
    Query parameters:
    - ?category=1 - filter by category ID
    - ?is_featured=true - show only featured products
    - ?is_bestseller=true - show only bestsellers
    - ?brand=Apple - filter by brand
    - ?search=iphone - search products
    - ?ordering=-created_at - order by date (newest first)
    - ?ordering=price - order by price (lowest first)
    - ?min_price=100 - filter products >= $100
    - ?max_price=500 - filter products <= $500
    - ?in_stock=true - only in-stock products
    - ?page=1 - pagination
    """
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'brand', 'is_featured', 'is_bestseller', 'is_new']
    search_fields = ['name', 'description', 'brand', 'sku']
    ordering_fields = ['name', 'base_price', 'created_at', 'rating']
    ordering = ['-created_at']  # newest first
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail views."""
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductDetailSerializer
    
    def get_queryset(self):
        """
        Optimize queries with select_related and prefetch_related.
        Only return active products.
        """
        queryset = Product.objects.filter(is_active=True).select_related(
            'category'
        ).prefetch_related(
            'variants',
            'variants__images',
            'images'
        )
        
        # Add price range filtering if provided
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(
                    Q(base_price__gte=min_price) |
                    Q(variants__price__gte=min_price)
                )
            except (ValueError, TypeError):
                pass
        
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(
                    Q(base_price__lte=max_price) |
                    Q(variants__price__lte=max_price)
                )
            except (ValueError, TypeError):
                pass
        
        # Filter by stock status if requested
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(
                Q(stock__gt=0) | Q(variants__stock__gt=0)
            )
        
        return queryset.distinct()
    
    @action(detail=True, methods=['get'])
    def variants(self, request, pk=None):
        """Get all variants for a product."""
        product = self.get_object()
        variants = product.variants.filter(is_active=True)
        serializer = ProductVariantSerializer(
            variants,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        """Get all images for a product."""
        product = self.get_object()
        images = product.images.all()
        serializer = ProductImageSerializer(
            images,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get all featured products."""
        products = self.get_queryset().filter(is_featured=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """Get all bestseller products."""
        products = self.get_queryset().filter(is_bestseller=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new(self, request):
        """Get newly added products."""
        products = self.get_queryset().filter(is_new=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for product variants.
    
    Note: Variants are usually accessed via nested endpoint in ProductViewSet,
    but this is available for direct API access if needed.
    """
    
    queryset = ProductVariant.objects.filter(is_active=True).select_related(
        'product'
    ).prefetch_related('images')
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'is_default', 'is_active']
    search_fields = ['sku', 'product__name']
    ordering_fields = ['sku', 'price', 'stock']
    ordering = ['product', 'ordering']

