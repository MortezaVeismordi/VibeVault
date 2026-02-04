#!/usr/bin/env python
"""
API Endpoint Test Script for Step 4
Tests all API endpoints and filters
"""
import os
import sys
import django

# Add the proshop directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proshop'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proshop.settings.base')
django.setup()

from django.test import Client
import json

client = Client()
BASE_URL = 'http://localhost:8000/shop/api'

def test_endpoint(name, path, params=None):
    """Test an API endpoint and print results"""
    full_path = f"/shop/api{path}"
    query_string = ""
    if params:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        full_path += f"?{query_string}"
    
    response = client.get(full_path)
    status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
    
    try:
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            count = len(data['results'])
            print(f"{status} | {name:50} | {count} items")
        elif isinstance(data, dict) and 'count' in data:
            print(f"{status} | {name:50} | {data['count']} total")
        elif isinstance(data, dict):
            print(f"{status} | {name:50} | ✓ OK")
        elif isinstance(data, list):
            print(f"{status} | {name:50} | {len(data)} items")
    except:
        print(f"{status} | {name:50} | No JSON response")
    
    return response.status_code == 200

# Run tests
print("\n" + "="*80)
print("STEP 4: REST API ENDPOINT TESTS")
print("="*80 + "\n")

results = {}

# Product Endpoints
print("[PRODUCT ENDPOINTS]")
print("-" * 80)
results['products_list'] = test_endpoint(
    "List Products (Paginated, 20/page)",
    "/products/"
)
results['products_list_page2'] = test_endpoint(
    "List Products - Page 2",
    "/products/",
    {'page': '2'}
)
results['products_featured'] = test_endpoint(
    "Featured Products",
    "/products/featured/"
)
results['products_bestsellers'] = test_endpoint(
    "Bestseller Products",
    "/products/bestsellers/"
)
results['products_new'] = test_endpoint(
    "New Products",
    "/products/new/"
)
results['products_detail'] = test_endpoint(
    "Product Detail (ID=1)",
    "/products/1/"
)
results['products_variants'] = test_endpoint(
    "Product Variants (ID=1)",
    "/products/1/variants/"
)
results['products_images'] = test_endpoint(
    "Product Images (ID=1)",
    "/products/1/images/"
)

# Filtering
print("\n[FILTERING & SEARCH]")
print("-" * 80)
results['filter_category'] = test_endpoint(
    "Filter by Category (category=1)",
    "/products/",
    {'category': '1'}
)
results['filter_brand'] = test_endpoint(
    "Filter by Brand (brand=Apple)",
    "/products/",
    {'brand': 'Apple'}
)
results['filter_featured'] = test_endpoint(
    "Filter Featured (is_featured=true)",
    "/products/",
    {'is_featured': 'true'}
)
results['filter_bestseller'] = test_endpoint(
    "Filter Bestseller (is_bestseller=true)",
    "/products/",
    {'is_bestseller': 'true'}
)
results['filter_new'] = test_endpoint(
    "Filter New (is_new=true)",
    "/products/",
    {'is_new': 'true'}
)

# Search
print("\n[SEARCH]")
print("-" * 80)
results['search_shirt'] = test_endpoint(
    "Search 'shirt'",
    "/products/",
    {'search': 'shirt'}
)
results['search_wireless'] = test_endpoint(
    "Search 'wireless'",
    "/products/",
    {'search': 'wireless'}
)
results['search_tshirt'] = test_endpoint(
    "Search by SKU 'TSHIRT'",
    "/products/",
    {'search': 'TSHIRT'}
)

# Price Range
print("\n[PRICE FILTERING]")
print("-" * 80)
results['price_min'] = test_endpoint(
    "Min Price Filter (min_price=20)",
    "/products/",
    {'min_price': '20'}
)
results['price_range'] = test_endpoint(
    "Price Range (min_price=20&max_price=100)",
    "/products/",
    {'min_price': '20', 'max_price': '100'}
)
results['price_max'] = test_endpoint(
    "Max Price Filter (max_price=50)",
    "/products/",
    {'max_price': '50'}
)

# Sorting
print("\n[ORDERING/SORTING]")
print("-" * 80)
results['order_name'] = test_endpoint(
    "Order by Name",
    "/products/",
    {'ordering': 'name'}
)
results['order_price'] = test_endpoint(
    "Order by Price (ascending)",
    "/products/",
    {'ordering': 'base_price'}
)
results['order_price_desc'] = test_endpoint(
    "Order by Price (descending)",
    "/products/",
    {'ordering': '-base_price'}
)
results['order_rating'] = test_endpoint(
    "Order by Rating",
    "/products/",
    {'ordering': 'rating'}
)
results['order_date'] = test_endpoint(
    "Order by Date (newest)",
    "/products/",
    {'ordering': '-created_at'}
)

# Stock
print("\n[STOCK FILTERING]")
print("-" * 80)
results['in_stock'] = test_endpoint(
    "In Stock Products (in_stock=true)",
    "/products/",
    {'in_stock': 'true'}
)

# Category Endpoints
print("\n[CATEGORY ENDPOINTS]")
print("-" * 80)
results['categories_list'] = test_endpoint(
    "List Categories",
    "/categories/"
)
results['categories_detail'] = test_endpoint(
    "Category Detail (ID=1)",
    "/categories/1/"
)
results['categories_products'] = test_endpoint(
    "Category Products (ID=1)",
    "/categories/1/products/"
)

# Variant Endpoints
print("\n[VARIANT ENDPOINTS]")
print("-" * 80)
results['variants_list'] = test_endpoint(
    "List Variants",
    "/variants/"
)
results['variants_detail'] = test_endpoint(
    "Variant Detail (ID=1)",
    "/variants/1/"
)
results['variants_by_product'] = test_endpoint(
    "Variants by Product (product=1)",
    "/variants/",
    {'product': '1'}
)

# Combined Filters
print("\n[COMBINED FILTERS]")
print("-" * 80)
results['combined_1'] = test_endpoint(
    "Featured + Category + Price Range",
    "/products/",
    {'is_featured': 'true', 'category': '1', 'min_price': '10', 'max_price': '500'}
)
results['combined_2'] = test_endpoint(
    "Search + Order by Price",
    "/products/",
    {'search': 'shirt', 'ordering': 'base_price'}
)
results['combined_3'] = test_endpoint(
    "Category + In Stock + Order by Rating",
    "/products/",
    {'category': '1', 'in_stock': 'true', 'ordering': '-rating'}
)

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

passed = sum(1 for v in results.values() if v)
total = len(results)

print(f"\nPassed: {passed}/{total}")
print(f"Failed: {total - passed}/{total}")

if passed == total:
    print("\nALL TESTS PASSED! API is fully functional.\n")
else:
    print("\nSome tests failed. Check the output above.\n")

# Print sample response
print("\n" + "="*80)
print("SAMPLE RESPONSE: Products List")
print("="*80 + "\n")
response = client.get("/shop/api/products/?page=1")
if response.status_code == 200:
    data = response.json()
    print(json.dumps({
        'count': data.get('count'),
        'page_size': len(data.get('results', [])),
        'next': data.get('next'),
        'previous': data.get('previous'),
        'first_result': data.get('results', [{}])[0] if data.get('results') else None
    }, indent=2, default=str))
