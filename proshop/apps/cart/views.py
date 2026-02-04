"""
Cart ViewSets and API endpoints for shopping cart management.
"""
import uuid
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
    CheckoutSessionSerializer,
)
from apps.shop.models import ProductVariant


class IsAnonymousOrAuthenticated(permissions.BasePermission):
    """
    Permission to allow both anonymous and authenticated users.
    """
    def has_permission(self, request, view):
        return True


class CartViewSet(viewsets.ViewSet):
    """
    API endpoints for shopping cart management.
    
    Supports:
    - GET /api/cart/ → Get current cart
    - POST /api/cart/add/ → Add item to cart
    - PATCH /api/cart/items/<id>/ → Update item quantity
    - DELETE /api/cart/items/<id>/ → Remove item from cart
    - DELETE /api/cart/ → Clear entire cart
    - POST /api/cart/checkout/ → Create checkout session
    
    Anonymous users: Cart stored per session
    Authenticated users: Cart linked to user account
    """
    
    permission_classes = [IsAnonymousOrAuthenticated]
    
    def _get_cart_for_user_or_session(self, request):
        """
        Get or create cart for user or session.
        
        Returns:
            Cart object
        """
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create_for_user(request.user)
        else:
            # Use session key for anonymous users
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart = Cart.objects.get_or_create_for_session(session_key)
        
        return cart
    
    def list(self, request):
        """
        GET /api/cart/ - Get current cart details
        """
        cart = self._get_cart_for_user_or_session(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """
        POST /api/cart/add/ - Add item to cart
        
        Request body:
        {
            "variant_id": 1,
            "quantity": 2
        }
        """
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        variant_id = serializer.validated_data['variant_id']
        quantity = serializer.validated_data['quantity']
        
        try:
            variant = ProductVariant.objects.select_related('product').get(
                id=variant_id,
                is_active=True
            )
        except ProductVariant.DoesNotExist:
            return Response(
                {'error': 'Variant not found or inactive'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock
        if quantity > variant.stock:
            return Response(
                {
                    'error': f'Insufficient stock. Available: {variant.stock}, Requested: {quantity}',
                    'available_stock': variant.stock
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart = self._get_cart_for_user_or_session(request)
        
        # Use atomic transaction to prevent race conditions
        with transaction.atomic():
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                variant=variant,
                defaults={
                    'quantity': quantity,
                    'price_at_add': variant.price,
                }
            )
            
            if not created:
                # Item already in cart, increase quantity
                new_quantity = cart_item.quantity + quantity
                if new_quantity > variant.stock:
                    return Response(
                        {
                            'error': f'Cannot add {quantity} more items. Total would exceed stock.',
                            'current_quantity': cart_item.quantity,
                            'available_stock': variant.stock
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                cart_item.quantity = new_quantity
                cart_item.save()
        
        # Refresh cart from database
        cart.refresh_from_db()
        serializer = CartSerializer(cart)
        return Response(
            {
                'message': f'Added {quantity} {variant.sku} to cart',
                'cart': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['patch'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, item_id=None):
        """
        PATCH /api/cart/items/<id>/ - Update item quantity
        
        Request body:
        {
            "quantity": 5
        }
        """
        cart = self._get_cart_for_user_or_session(request)
        
        try:
            cart_item = cart.items.get(id=item_id)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_quantity = serializer.validated_data['quantity']
        
        # Check stock
        if new_quantity > cart_item.variant.stock:
            return Response(
                {
                    'error': f'Insufficient stock. Available: {cart_item.variant.stock}',
                    'available_stock': cart_item.variant.stock
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = new_quantity
        cart_item.save()
        
        # Refresh and return updated cart
        cart.refresh_from_db()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """
        DELETE /api/cart/items/<id>/ - Remove item from cart
        """
        cart = self._get_cart_for_user_or_session(request)
        
        try:
            cart_item = cart.items.get(id=item_id)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        variant_sku = cart_item.variant.sku
        cart_item.delete()
        
        # Refresh and return updated cart
        cart.refresh_from_db()
        serializer = CartSerializer(cart)
        return Response(
            {
                'message': f'Removed {variant_sku} from cart',
                'cart': serializer.data
            }
        )
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """
        DELETE /api/cart/ - Clear entire cart
        """
        cart = self._get_cart_for_user_or_session(request)
        item_count = cart.items.count()
        cart.clear()
        
        return Response(
            {
                'message': f'Cleared {item_count} items from cart',
                'cart': CartSerializer(cart).data
            }
        )
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        POST /api/cart/checkout/ - Create checkout session
        
        This creates a checkout session for payment processing.
        In a real implementation, this would integrate with Stripe/PayPal API.
        
        Returns:
        {
            "session_id": "uuid",
            "checkout_url": "https://checkout.example.com/session",
            "total_amount": 150.00,
            "items_count": 3
        }
        """
        cart = self._get_cart_for_user_or_session(request)
        
        # Validate cart has items
        if not cart.has_items:
            return Response(
                {'error': 'Cannot checkout with empty cart'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check all items are still in stock
        out_of_stock_items = []
        for item in cart.items.all():
            if not item.is_in_stock():
                out_of_stock_items.append({
                    'sku': item.variant.sku,
                    'requested': item.quantity,
                    'available': item.variant.stock
                })
        
        if out_of_stock_items:
            return Response(
                {
                    'error': 'Some items are no longer in stock',
                    'out_of_stock': out_of_stock_items
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create checkout session (in real app, would create Stripe/PayPal session)
        session_id = str(uuid.uuid4())
        
        # Store session data (could use Django sessions or database)
        # For now, just return the session info
        checkout_data = {
            'session_id': session_id,
            'checkout_url': f'https://checkout.example.com/session/{session_id}',
            'total_amount': float(cart.total_price),
            'items_count': cart.total_items,
        }
        
        serializer = CheckoutSessionSerializer(checkout_data)
        return Response(
            {
                'message': 'Checkout session created successfully',
                'checkout': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
