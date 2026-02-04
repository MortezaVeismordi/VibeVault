#!/usr/bin/env python
"""
Step 7: Complete E-to-E Testing Script
Tests the full checkout flow: Cart -> Order -> Payment -> Stripe Webhook

Run with: python STEP7_TEST_FLOW.py
"""

import os
import django
import requests
import json
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proshop.settings.development')
django.setup()

from apps.shop.models import Product, ProductVariant
from apps.accounts.models import CustomUser
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.payment.models import Payment


BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
}


def test_anonymous_cart_flow():
    """Test anonymous user cart and checkout"""
    print("\n" + "="*60)
    print("TEST 1: Anonymous User Flow")
    print("="*60)
    
    session = requests.Session()
    
    # Step 1: Get initial session (anonymous)
    print("\n[1] Getting session for anonymous user...")
    resp = session.get(f"{BASE_URL}/api/cart/")
    print(f"    Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"    Session key: {session.cookies.get('sessionid', 'N/A')[:20]}...")
    
    # Step 2: Get products
    print("\n[2] Fetching products...")
    resp = session.get(f"{BASE_URL}/api/shop/products/")
    if resp.status_code == 200:
        products = resp.json()
        print(f"    Total products: {len(products)}")
        if isinstance(products, list) and len(products) > 0:
            product_id = products[0].get('id')
            print(f"    First product ID: {product_id}")
        else:
            print(f"    ERROR: Unexpected response format: {products}")
            return
    else:
        print(f"    ERROR: {resp.status_code}")
        print(f"    Response: {resp.text}")
        return
    
    # Step 3: Get variants for product
    print(f"\n[3] Fetching variants for product {product_id}...")
    resp = session.get(f"{BASE_URL}/api/shop/products/{product_id}/variants/")
    if resp.status_code == 200:
        variants = resp.json()
        print(f"    Total variants: {len(variants)}")
        if isinstance(variants, list) and len(variants) > 0:
            variant_id = variants[0].get('id')
            print(f"    First variant ID: {variant_id}")
        else:
            print(f"    ERROR: Unexpected response format")
            return
    else:
        print(f"    ERROR: {resp.status_code}")
        return
    
    # Step 4: Add to cart
    print(f"\n[4] Adding variant {variant_id} to cart (quantity=2)...")
    resp = session.post(
        f"{BASE_URL}/api/cart/add/",
        json={"variant_id": variant_id, "quantity": 2},
        headers=HEADERS
    )
    print(f"    Status: {resp.status_code}")
    if resp.status_code in [200, 201]:
        print(f"    Response: {resp.json()}")
    else:
        print(f"    ERROR: {resp.text}")
        return
    
    # Step 5: View cart
    print(f"\n[5] Viewing cart...")
    resp = session.get(f"{BASE_URL}/api/cart/")
    if resp.status_code == 200:
        cart_data = resp.json()
        print(f"    Items count: {cart_data.get('items_count', 'N/A')}")
        print(f"    Total: ${cart_data.get('total', 'N/A')}")
        print(f"    Items: {len(cart_data.get('items', []))} items")
    else:
        print(f"    ERROR: {resp.text}")
        return
    
    # Step 6: Create checkout (POST /api/payment/checkout/)
    print(f"\n[6] Creating Stripe checkout session...")
    resp = session.post(
        f"{BASE_URL}/api/payment/checkout/",
        json={},
        headers=HEADERS
    )
    print(f"    Status: {resp.status_code}")
    if resp.status_code in [200, 201]:
        checkout_data = resp.json()
        print(f"    Session ID: {checkout_data.get('session_id', 'N/A')[:20]}...")
        print(f"    Checkout URL: {checkout_data.get('checkout_url', 'N/A')[:50]}...")
        print(f"    Total Amount: ${checkout_data.get('total_amount', 'N/A')}")
        print(f"    Items Count: {checkout_data.get('items_count', 'N/A')}")
        
        session_id = checkout_data.get('session_id')
        return session_id
    else:
        print(f"    ERROR: {resp.text}")
        return None


def test_authenticated_flow():
    """Test authenticated user flow"""
    print("\n" + "="*60)
    print("TEST 2: Authenticated User Flow")
    print("="*60)
    
    # Create test user if not exists
    user_email = "testuser@proshop.test"
    user_password = "testpass123!@#"
    
    user, created = CustomUser.objects.get_or_create(
        email=user_email,
        defaults={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )
    if created:
        user.set_password(user_password)
        user.save()
        print(f"\n[AUTH] Created new test user: {user_email}")
    else:
        print(f"\n[AUTH] Using existing test user: {user_email}")
    
    # Create session with auth token
    session = requests.Session()
    
    # Try to login (check if there's a login endpoint)
    print(f"\n[1] Attempting to authenticate...")
    resp = session.post(
        f"{BASE_URL}/api/accounts/login/",
        json={"email": user_email, "password": user_password},
        headers=HEADERS
    )
    print(f"    Status: {resp.status_code}")
    if resp.status_code in [200, 201]:
        print(f"    Auth successful")
        print(f"    Response keys: {list(resp.json().keys())}")
    else:
        print(f"    Note: Login endpoint may not exist (expected for API-only)")
        print(f"    Will use session-based auth instead")
    
    # Get products
    print(f"\n[2] Fetching products...")
    resp = session.get(f"{BASE_URL}/api/shop/products/")
    if resp.status_code == 200:
        products = resp.json()
        if len(products) > 0:
            product_id = products[0].get('id')
            print(f"    First product ID: {product_id}")
        else:
            print(f"    ERROR: No products")
            return
    else:
        print(f"    ERROR: {resp.status_code}")
        return
    
    # Get variants
    print(f"\n[3] Fetching variants...")
    resp = session.get(f"{BASE_URL}/api/shop/products/{product_id}/variants/")
    if resp.status_code == 200:
        variants = resp.json()
        if len(variants) > 1:
            variant_id = variants[1].get('id')
            print(f"    Variant ID (2nd variant): {variant_id}")
        else:
            variant_id = variants[0].get('id')
            print(f"    Variant ID (1st variant): {variant_id}")
    else:
        print(f"    ERROR: {resp.status_code}")
        return
    
    # Add to cart
    print(f"\n[4] Adding variant {variant_id} to cart (quantity=1)...")
    resp = session.post(
        f"{BASE_URL}/api/cart/add/",
        json={"variant_id": variant_id, "quantity": 1},
        headers=HEADERS
    )
    print(f"    Status: {resp.status_code}")
    
    # Create checkout
    print(f"\n[5] Creating Stripe checkout session...")
    resp = session.post(
        f"{BASE_URL}/api/payment/checkout/",
        json={},
        headers=HEADERS
    )
    print(f"    Status: {resp.status_code}")
    if resp.status_code in [200, 201]:
        checkout_data = resp.json()
        print(f"    Session ID: {checkout_data.get('session_id', 'N/A')[:20]}...")
        session_id = checkout_data.get('session_id')
        return session_id
    else:
        print(f"    ERROR: {resp.text}")
        return None


def test_payment_status(session_id):
    """Test payment status endpoint"""
    if not session_id:
        print("\n[STATUS] Skipping (no session_id)")
        return
    
    print("\n" + "="*60)
    print("TEST 3: Payment Status Check")
    print("="*60)
    
    print(f"\n[1] Checking status for session {session_id[:20]}...")
    resp = requests.get(
        f"{BASE_URL}/api/payment/status/?session_id={session_id}",
        headers=HEADERS
    )
    print(f"    Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"    Stripe Status: {data.get('stripe_status', 'N/A')}")
        print(f"    Order ID: {data.get('order_number', 'N/A')}")
        print(f"    Payment Status: {data.get('payment_status', 'N/A')}")
        print(f"    Amount: ${data.get('amount', 'N/A')}")
    else:
        print(f"    ERROR: {resp.text}")


def test_database_state():
    """Check database state after tests"""
    print("\n" + "="*60)
    print("TEST 4: Database State Verification")
    print("="*60)
    
    carts = Cart.objects.all()
    print(f"\n[CARTS] Total: {carts.count()}")
    for cart in carts[:2]:
        print(f"  - ID: {cart.id}, Items: {cart.items.count()}")
    
    orders = Order.objects.all()
    print(f"\n[ORDERS] Total: {orders.count()}")
    for order in orders[:2]:
        print(f"  - Number: {order.order_number}, Status: {order.status}, Stripe Session: {order.stripe_session_id}")
    
    payments = Payment.objects.all()
    print(f"\n[PAYMENTS] Total: {payments.count()}")
    for payment in payments[:2]:
        print(f"  - ID: {payment.id}, Status: {payment.status}, Stripe Session: {payment.stripe_session_id}")


def main():
    print("\n")
    print("*" * 60)
    print("STEP 7: COMPLETE END-TO-END TESTING")
    print("*" * 60)
    
    try:
        # Test anonymous flow
        session_id_1 = test_anonymous_cart_flow()
        test_payment_status(session_id_1)
        
        # Test authenticated flow
        session_id_2 = test_authenticated_flow()
        test_payment_status(session_id_2)
        
        # Check database state
        test_database_state()
        
        print("\n" + "*" * 60)
        print("TESTING COMPLETE!")
        print("*" * 60)
        print("\nNEXT STEPS:")
        print("1. Manually complete payment at Stripe checkout URL")
        print("2. Use Stripe CLI to verify webhook: stripe listen")
        print("3. Check database to verify Order/Payment updates")
        print("4. Verify stock was reduced after payment success")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
