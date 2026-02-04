from django.db import models
from django.conf import settings
from decimal import Decimal
from apps.shop.models import Product, ProductVariant


class CartManager(models.Manager):
    """Custom manager for Cart model"""
    
    def get_or_create_for_user(self, user):
        """Get or create cart for authenticated user"""
        cart, created = self.get_or_create(user=user)
        return cart
    
    def get_or_create_for_session(self, session_key):
        """Get or create cart for anonymous user (session-based)"""
        cart, created = self.get_or_create(
            session_id=session_key,
            user=None
        )
        return cart


class Cart(models.Model):
    """Shopping cart for anonymous or authenticated users"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='cart'
    )
    session_id = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        db_index=True,
        help_text="Session key for anonymous users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CartManager()
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_id']),
            models.Index(fields=['updated_at']),
        ]
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart for {self.session_id}"
    
    @property
    def total_items(self):
        """Total quantity of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Total price of all items"""
        return sum(item.get_subtotal() for item in self.items.all())
    
    @property
    def has_items(self):
        """Check if cart has any items"""
        return self.items.exists()
    
    def clear(self):
        """Empty the cart"""
        self.items.all().delete()
    
    def merge_from_session(self, session_key):
        """
        Merge items from session cart to user cart
        Used when user logs in
        """
        if not self.user or not session_key:
            return
        
        try:
            session_cart = Cart.objects.get(session_id=session_key, user=None)
            for item in session_cart.items.all():
                # Try to get existing item in user cart
                cart_item, created = CartItem.objects.get_or_create(
                    cart=self,
                    variant=item.variant,
                    defaults={
                        'quantity': item.quantity,
                        'price_at_add': item.price_at_add,
                    }
                )
                if not created:
                    # If item exists, increase quantity
                    cart_item.quantity += item.quantity
                    cart_item.save()
            
            # Delete session cart
            session_cart.delete()
        except Cart.DoesNotExist:
            pass


class CartItem(models.Model):
    """Individual items in the shopping cart"""
    
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of this variant"
    )
    price_at_add = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price captured when item was added"
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'variant')
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['variant']),
        ]
    
    def __str__(self):
        return f"{self.variant.product.name} ({self.variant.sku}) x{self.quantity}"
    
    @property
    def product(self):
        """Get the product from variant"""
        return self.variant.product
    
    def get_subtotal(self):
        """Get total price for this item (price_at_add * quantity)"""
        return self.price_at_add * self.quantity
    
    def is_in_stock(self):
        """Check if requested quantity is available"""
        return self.variant.stock >= self.quantity
