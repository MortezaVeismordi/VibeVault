from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_id')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('product__name', 'cart__user__username')
