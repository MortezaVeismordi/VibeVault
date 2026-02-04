#!/usr/bin/env python
"""
Comprehensive Cart API Test Suite
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proshop.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import json
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.shop.models import Product, ProductVariant, Category
from apps.cart.models import Cart, CartItem

User = get_user_model()
client = APIClient()
BASE_URL = 'http://localhost:8000/api/cart'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_test(name, passed, response=None):
    symbol = f"{Colors.GREEN}✓{Colors.RESET}" if passed else f"{Colors.RED}✗{Colors.RESET}"
    print(f"{symbol} {name}")
    if response and not passed:
        print(f"  Status: {response.status_code}")
        try:
            print(f"  Error: {json.dumps(response.json(), indent=4, default=str)}")
        except:
            print(f"  Response: {response.text}")

def setup_test_data():
    """Create test data"""
    print_header("Setting Up Test Data")
    
    # Create admin user if needed
    admin, _ = User.objects.get_or_create(
        email='admin@test.com',
        defaults={'username': 'admin', 'first_name': 'Admin'}
    )
    if _:
        admin.set_password('admin123')
        admin.save()
        print(f"  Created admin user: {admin.email}")
    
    # Create category
    category, _ = Category.objects.get_or_create(
        slug='test-products',
        defaults={'name': 'Test Products'}
    )
    
    # Create product
    product, _ = Product.objects.get_or_create(
        slug='test-product',
        defaults={
            'name': 'Test T-Shirt',
            'description': 'A test product for cart API',
            'category': category,
            'is_featured': True,
            'created_by': admin
        }
    )
    
    # Create variants
    variants_data = [
        {'sku': 'TSHIRT-RED-S', 'name': 'Red - Size S', 'price': '19.99', 'stock': 10},
        {'sku': 'TSHIRT-BLUE-M', 'name': 'Blue - Size M', 'price': '19.99', 'stock': 5},
        {'sku': 'TSHIRT-GREEN-L', 'name': 'Green - Size L', 'price': '19.99', 'stock': 20},
    ]
    
    variants = []
    for data in variants_data:
        variant, created = ProductVariant.objects.get_or_create(
            sku=data['sku'],
            product=product,
            defaults={
                'name': data['name'],
                'price': data['price'],
                'stock': data['stock'],
                'is_active': True,
            }
        )
        variants.append(variant)
        status = "Created" if created else "Found"
        print(f"  {status}: {data['sku']} (stock={data['stock']})")
    
    return variants

def test_anonymous_cart():
    """Test anonymous cart operations"""
    print_header("Test 1: Anonymous Cart")
    
    # Clear any existing session carts
    Cart.objects.filter(user=None).delete()
    
    variants = ProductVariant.objects.filter(is_active=True, sku__startswith='TSHIRT')[:2]
    if len(variants) < 2:
        print(f"{Colors.RED}✗ Not enough variants for testing{Colors.RESET}")
        return
    
    variant1, variant2 = variants[0], variants[1]
    
    # Test 1.1: Get empty cart
    print("\n1.1 Get empty cart:")
    response = client.get(f'{BASE_URL}/')
    success = response.status_code == 200
    print_test("GET /api/cart/", success, response)
    if not success:
        return
    
    cart_data = response.json()
    print(f"  Cart ID: {cart_data.get('id')}")
    print(f"  Items: {cart_data.get('items', [])}")
    print(f"  Total: ${cart_data.get('total_price', 0)}")
    
    # Test 1.2: Add first item
    print("\n1.2 Add first item to cart:")
    payload = {'variant_id': variant1.id, 'quantity': 2}
    response = client.post(f'{BASE_URL}/add/', payload, format='json')
    success = response.status_code == 201
    print_test("POST /api/cart/add/", success, response)
    if success:
        result = response.json()
        print(f"  Message: {result.get('message', '')}")
    
    # Test 1.3: Get cart with items
    print("\n1.3 Get cart after adding item:")
    response = client.get(f'{BASE_URL}/')
    success = response.status_code == 200
    print_test("GET /api/cart/", success, response)
    if success:
        cart_data = response.json()
        items = cart_data.get('items', [])
        print(f"  Total items: {len(items)}")
        print(f"  Total price: ${cart_data.get('total_price', 0)}")
        if items:
            item_id = items[0]['id']
            
            # Test 1.4: Update item quantity
            print("\n1.4 Update item quantity:")
            response = client.patch(f'{BASE_URL}/items/{item_id}/', {'quantity': 3}, format='json')
            success = response.status_code == 200
            print_test(f"PATCH /api/cart/items/{item_id}/", success, response)
            if success:
                updated = response.json()
                print(f"  New quantity in cart: {updated['items'][0]['quantity']}")
            
            # Test 1.5: Add second item
            print("\n1.5 Add second item:")
            payload = {'variant_id': variant2.id, 'quantity': 1}
            response = client.post(f'{BASE_URL}/add/', payload, format='json')
            success = response.status_code == 201
            print_test("POST /api/cart/add/", success, response)
            if success:
                cart_data = response.json()['cart']
                items = cart_data.get('items', [])
                print(f"  Items in cart: {len(items)}")
                
                if len(items) > 1:
                    item_id_2 = items[1]['id']
                    
                    # Test 1.6: Remove second item
                    print("\n1.6 Remove item:")
                    response = client.delete(f'{BASE_URL}/items/{item_id_2}/')
                    success = response.status_code == 200
                    print_test(f"DELETE /api/cart/items/{item_id_2}/", success, response)
                    if success:
                        print(f"  Items remaining: {len(response.json()['cart']['items'])}")
    
    # Test 1.7: Checkout
    print("\n1.7 Create checkout session:")
    response = client.post(f'{BASE_URL}/checkout/', {}, format='json')
    success = response.status_code == 201
    print_test("POST /api/cart/checkout/", success, response)
    if success:
        checkout = response.json().get('checkout', {})
        print(f"  Session ID: {checkout.get('session_id', '')[:8]}...")
        print(f"  Total: ${checkout.get('total_amount', 0)}")
        print(f"  Items: {checkout.get('items_count', 0)}")
    
    # Test 1.8: Clear cart
    print("\n1.8 Clear entire cart:")
    response = client.delete(f'{BASE_URL}/')
    success = response.status_code == 200
    print_test("DELETE /api/cart/", success, response)
    if success:
        result = response.json()
        print(f"  Cleared items: {result.get('message', '')}")

def test_stock_validation():
    """Test stock validation"""
    print_header("Test 2: Stock Validation")
    
    variant = ProductVariant.objects.filter(is_active=True, stock__gt=0, sku__startswith='TSHIRT').first()
    if not variant:
        print(f"{Colors.RED}✗ No variants with stock found{Colors.RESET}")
        return
    
    print(f"Using variant: {variant.sku} (available stock: {variant.stock})")
    
    # Test 2.1: Try to add more than available
    print("\n2.1 Try adding more items than available:")
    payload = {'variant_id': variant.id, 'quantity': variant.stock + 10}
    response = client.post(f'{BASE_URL}/add/', payload, format='json')
    success = response.status_code == 400
    print_test(f"POST /api/cart/add/ (qty > stock)", success, response)
    if success:
        error = response.json()
        print(f"  Error: {error.get('error', '')}")
    
    # Test 2.2: Add valid quantity
    print("\n2.2 Add valid quantity:")
    payload = {'variant_id': variant.id, 'quantity': 2}
    response = client.post(f'{BASE_URL}/add/', payload, format='json')
    success = response.status_code == 201
    print_test("POST /api/cart/add/ (valid qty)", success, response)

def test_authenticated_cart():
    """Test authenticated user cart"""
    print_header("Test 3: Authenticated User Cart")
    
    # Create test user
    user, created = User.objects.get_or_create(
        email='testuser@test.com',
        defaults={'username': 'testuser', 'first_name': 'Test'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created test user: {user.email}\n")
    
    # Clear user's existing cart
    Cart.objects.filter(user=user).delete()
    
    # Login
    client.force_authenticate(user=user)
    print(f"Authenticated as: {user.email}\n")
    
    variant = ProductVariant.objects.filter(is_active=True, sku__startswith='TSHIRT').first()
    if not variant:
        print(f"{Colors.RED}✗ No variants found{Colors.RESET}")
        return
    
    # Test 3.1: Get empty cart for user
    print("3.1 Get empty authenticated cart:")
    response = client.get(f'{BASE_URL}/')
    success = response.status_code == 200
    print_test("GET /api/cart/", success, response)
    if not success:
        return
    
    print(f"  Cart is for user: {response.json().get('user_id') == user.id}")
    
    # Test 3.2: Add item
    print("\n3.2 Add item to authenticated cart:")
    payload = {'variant_id': variant.id, 'quantity': 3}
    response = client.post(f'{BASE_URL}/add/', payload, format='json')
    success = response.status_code == 201
    print_test("POST /api/cart/add/", success, response)
    if success:
        print(f"  Item added: {variant.sku}")
    
    # Test 3.3: Get authenticated cart
    print("\n3.3 Get authenticated cart with items:")
    response = client.get(f'{BASE_URL}/')
    success = response.status_code == 200
    print_test("GET /api/cart/", success, response)
    if success:
        cart_data = response.json()
        items = cart_data.get('items', [])
        print(f"  Items: {len(items)}")
        print(f"  Total: ${cart_data.get('total_price', 0)}")
        print(f"  User ID: {cart_data.get('user_id')}")

def test_merge_logic():
    """Test session to user merge logic"""
    print_header("Test 4: Session to User Merge Logic")
    
    print("This test verifies the merge_from_session() method\n")
    
    from apps.shop.models import ProductVariant
    
    # Create test user
    user = User.objects.create_user(
        email='mergetest@test.com',
        username='mergetest',
        password='merge123'
    )
    
    # Get variants
    variants = ProductVariant.objects.filter(is_active=True, sku__startswith='TSHIRT')[:2]
    if len(variants) < 2:
        print(f"{Colors.YELLOW}⚠ Not enough variants for merge test{Colors.RESET}")
        return
    
    # Create session cart with items
    print("4.1 Creating session cart with items:")
    session_key = 'test-session-key-123'
    session_cart = Cart.objects.create(session_id=session_key, user=None)
    CartItem.objects.create(cart=session_cart, variant=variants[0], quantity=2, price_at_add=variants[0].price)
    CartItem.objects.create(cart=session_cart, variant=variants[1], quantity=1, price_at_add=variants[1].price)
    print(f"  Created session cart with 2 items")
    
    # Create user cart
    print("\n4.2 Creating user cart with existing items:")
    user_cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=user_cart, variant=variants[0], quantity=1, price_at_add=variants[0].price)
    print(f"  Created user cart with 1 item (same variant as session)")
    
    print(f"\n  Session cart items: {session_cart.items.count()}")
    print(f"  User cart items before merge: {user_cart.items.count()}")
    
    # Test merge
    print("\n4.3 Performing merge:")
    user_cart.merge_from_session(session_key)
    user_cart.refresh_from_db()
    
    print(f"  User cart items after merge: {user_cart.items.count()}")
    print(f"  Session cart exists: {Cart.objects.filter(session_id=session_key).exists()}")
    
    # Check if quantities merged correctly
    variant_items = user_cart.items.filter(variant=variants[0])
    if variant_items.exists():
        merged_qty = variant_items.first().quantity
        print(f"  {variants[0].sku} quantity: {merged_qty} (should be 3 = 1+2)")
        print_test("Merge logic working correctly", merged_qty == 3)
    else:
        print_test("Merge logic working correctly", False)

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔" + "="*58 + "╗")
    print("║" + " CART & CHECKOUT API TEST SUITE ".center(58) + "║")
    print("║" + " Comprehensive Cart Operations Testing ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    print(f"{Colors.RESET}")
    
    try:
        # Setup test data
        setup_test_data()
        
        # Run tests
        test_anonymous_cart()
        test_stock_validation()
        test_authenticated_cart()
        test_merge_logic()
        
        # Summary
        print_header("Test Suite Complete")
        print(f"{Colors.GREEN}All tests completed!{Colors.RESET}\n")
        print(f"API Endpoints tested:")
        print(f"  GET    /api/cart/")
        print(f"  POST   /api/cart/add/")
        print(f"  PATCH  /api/cart/items/<id>/")
        print(f"  DELETE /api/cart/items/<id>/")
        print(f"  DELETE /api/cart/")
        print(f"  POST   /api/cart/checkout/")
        print()
        
    except Exception as e:
        print(f"\n{Colors.RED}✗ Error during testing: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
