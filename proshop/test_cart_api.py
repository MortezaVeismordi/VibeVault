#!/usr/bin/env python
"""
Test script for Cart API endpoints
"""
import os
import sys
import django
import json
import requests
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proshop.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.shop.models import Product, ProductVariant, Category
from apps.accounts.models import CustomUser
from apps.cart.models import Cart, CartItem
from rest_framework.test import APIClient
from django.test import TestCase

# Create test client
client = APIClient()

BASE_URL = 'http://localhost:8000/api/cart'

def print_test(name, status, data=None):
    """Print test result"""
    symbol = "✓" if status else "✗"
    print(f"\n{symbol} {name}")
    if data:
        print(f"  Response: {json.dumps(data, indent=2, default=str)}")

def test_anonymous_cart():
    """Test anonymous cart operations"""
    print("\n" + "="*50)
    print("TESTING ANONYMOUS CART")
    print("="*50)
    
    # Get product variant
    variant = ProductVariant.objects.filter(is_active=True).first()
    if not variant:
        print("✗ No active variants found!")
        return
    
    print(f"Using variant: {variant.sku} (ID: {variant.id})")
    
    # Test 1: Get empty cart
    print("\n1. Getting empty cart...")
    response = client.get(f'{BASE_URL}/')
    print_test("GET /api/cart/", response.status_code == 200, response.json())
    
    # Test 2: Add item to cart
    print("\n2. Adding item to cart...")
    data = {
        'variant_id': variant.id,
        'quantity': 2
    }
    response = client.post(f'{BASE_URL}/add/', data, format='json')
    print_test(f"POST /api/cart/add/ (qty=2)", response.status_code == 201, response.json())
    
    # Test 3: Get cart after adding item
    print("\n3. Getting cart after adding item...")
    response = client.get(f'{BASE_URL}/')
    cart_data = response.json()
    print_test("GET /api/cart/ (with items)", response.status_code == 200, cart_data)
    
    if response.status_code == 200:
        items = cart_data.get('items', [])
        if items:
            item_id = items[0]['id']
            
            # Test 4: Update item quantity
            print(f"\n4. Updating item quantity (item_id={item_id})...")
            update_data = {'quantity': 5}
            response = client.patch(f'{BASE_URL}/items/{item_id}/', update_data, format='json')
            print_test(f"PATCH /api/cart/items/{item_id}/", response.status_code == 200, response.json())
            
            # Test 5: Remove item
            print(f"\n5. Removing item (item_id={item_id})...")
            response = client.delete(f'{BASE_URL}/items/{item_id}/')
            print_test(f"DELETE /api/cart/items/{item_id}/", response.status_code == 200, response.json())
    
    # Test 6: Add item again for checkout test
    print("\n6. Adding item again for checkout test...")
    response = client.post(f'{BASE_URL}/add/', {'variant_id': variant.id, 'quantity': 1}, format='json')
    print_test("POST /api/cart/add/ (qty=1)", response.status_code == 201, response.json())
    
    # Test 7: Checkout
    print("\n7. Creating checkout session...")
    response = client.post(f'{BASE_URL}/checkout/', {}, format='json')
    print_test("POST /api/cart/checkout/", response.status_code == 201, response.json())
    
    # Test 8: Clear cart
    print("\n8. Clearing cart...")
    response = client.delete(f'{BASE_URL}/')
    print_test("DELETE /api/cart/", response.status_code == 200, response.json())

def test_stock_validation():
    """Test stock validation"""
    print("\n" + "="*50)
    print("TESTING STOCK VALIDATION")
    print("="*50)
    
    # Get variant with limited stock
    variant = ProductVariant.objects.filter(is_active=True, stock__gt=0).first()
    if not variant:
        print("✗ No variants with stock found!")
        return
    
    print(f"Using variant: {variant.sku} (stock={variant.stock})")
    
    # Test requesting more than available
    print(f"\n1. Requesting {variant.stock + 10} units (available: {variant.stock})...")
    data = {
        'variant_id': variant.id,
        'quantity': variant.stock + 10
    }
    response = client.post(f'{BASE_URL}/add/', data, format='json')
    print_test("POST /api/cart/add/ (excessive qty)", response.status_code == 400, response.json())

def test_authenticated_cart():
    """Test authenticated user cart"""
    print("\n" + "="*50)
    print("TESTING AUTHENTICATED CART")
    print("="*50)
    
    # Create test user
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user, created = User.objects.get_or_create(
        email='testuser@example.com',
        defaults={'username': 'testuser', 'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Login
    print(f"\nLogging in as {user.email}...")
    client.force_authenticate(user=user)
    
    # Get product variant
    variant = ProductVariant.objects.filter(is_active=True).first()
    if not variant:
        print("✗ No active variants found!")
        return
    
    # Test 1: Get cart (should be empty initially)
    print("\n1. Getting cart for authenticated user...")
    response = client.get(f'{BASE_URL}/')
    print_test("GET /api/cart/", response.status_code == 200, response.json())
    
    # Test 2: Add item
    print(f"\n2. Adding {variant.sku} to authenticated cart...")
    data = {
        'variant_id': variant.id,
        'quantity': 3
    }
    response = client.post(f'{BASE_URL}/add/', data, format='json')
    print_test("POST /api/cart/add/", response.status_code == 201, response.json())
    
    # Test 3: Get cart
    print("\n3. Getting cart with items...")
    response = client.get(f'{BASE_URL}/')
    print_test("GET /api/cart/ (authenticated with items)", response.status_code == 200, response.json())

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CART API ENDPOINT TESTS")
    print("="*60)
    
    try:
        test_anonymous_cart()
        test_stock_validation()
        test_authenticated_cart()
        
        print("\n" + "="*60)
        print("TEST SUITE COMPLETE")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
