#!/usr/bin/env python
"""
Prepare test data for cart API testing
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proshop.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.shop.models import Product, ProductVariant, Category
from apps.accounts.models import CustomUser

def create_test_data():
    """Create test data"""
    print("Creating test data...")
    
    # Check if data already exists
    if ProductVariant.objects.filter(is_active=True).exists():
        print("✓ Test data already exists")
        variants = ProductVariant.objects.filter(is_active=True).values('id', 'sku', 'stock')
        for v in variants[:5]:
            print(f"  - {v['sku']}: ID={v['id']}, Stock={v['stock']}")
        return
    
    # Create category
    category, _ = Category.objects.get_or_create(
        slug='test-products',
        defaults={'name': 'Test Products', 'description': 'Test category'}
    )
    
    # Create product
    product, _ = Product.objects.get_or_create(
        slug='test-product',
        defaults={
            'name': 'Test Product',
            'description': 'A test product for cart API',
            'category': category,
            'is_featured': True,
            'created_by': CustomUser.objects.first() or CustomUser.objects.create_user(
                email='admin@test.com',
                username='admin',
                password='admin123'
            )
        }
    )
    
    # Create variants
    variants = [
        {'sku': 'TEST-001', 'name': 'Red - Size S', 'price': '29.99', 'stock': 10},
        {'sku': 'TEST-002', 'name': 'Blue - Size M', 'price': '29.99', 'stock': 5},
        {'sku': 'TEST-003', 'name': 'Green - Size L', 'price': '29.99', 'stock': 20},
    ]
    
    for v in variants:
        variant, created = ProductVariant.objects.get_or_create(
            sku=v['sku'],
            product=product,
            defaults={
                'name': v['name'],
                'price': v['price'],
                'stock': v['stock'],
                'is_active': True,
            }
        )
        status = "Created" if created else "Exists"
        print(f"✓ {status}: {v['sku']} (stock={v['stock']})")

if __name__ == '__main__':
    create_test_data()
