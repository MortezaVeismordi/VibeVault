# Step 5: Cart & Checkout API - Complete Documentation

## مرحله ۵: API مدیریت سبد خرید و Checkout

**وضعیت**: ✅ COMPLETE  
**تاریخ تکمیل**: 2025-02-04  
**نسخه**: 1.0

---

## 📋 فهرست مطالب

1. [معرفی](#معرفی)
2. [معماری سیستم](#معماری-سیستم)
3. [مدل‌ها (Models)](#مدلها-models)
4. [Serializers](#serializers)
5. [ViewSet و Endpoints](#viewset-و-endpoints)
6. [آزمایش API](#آزمایش-api)
7. [مثال‌های استفاده](#مثالهای-استفاده)
8. [پیاده‌سازی Merge Logic](#پیاده‌سازی-merge-logic)

---

## معرفی

مرحله ۵ یک **API کامل برای مدیریت سبد خرید** (Shopping Cart) فراهم می‌کند که:

✅ **پشتیبانی از کاربران ناشناس** (Anonymous)  
✅ **پشتیبانی از کاربران احراز شده** (Authenticated)  
✅ **اعتبارسنجی Stock** (تعداد موجودی)  
✅ **ادغام خودکار سبد** (Merge Logic) هنگام login  
✅ **ایجاد Checkout Session** برای پرداخت  
✅ **محاسبه خودکار** قیمت کل، تعداد اقلام  

---

## معماری سیستم

### ۱. Model Relationships

```
┌─────────────────┐         ┌──────────────────┐
│   CustomUser    │         │      Cart        │
│  (Authenticated)│◄───────►│  (OneToOne)      │
└─────────────────┘         └──────────────────┘
       │                            │
       │                            ├─ user (FK, nullable)
       │                            ├─ session_id (CharField)
       │                            ├─ created_at
       │                            └─ updated_at
       │
       │                     ┌──────────────────┐
       │                     │    CartItem      │
       │                     │   (Many Items)   │
       │                     ├─ cart (FK)      │
       │                     ├─ variant (FK)───┼──────┐
       │                     ├─ quantity       │      │
       │                     ├─ price_at_add   │      │
       │                     ├─ added_at       │      │
       │                     └─ updated_at     │      │
       │                                        │      │
       │                                        │      ▼
       │                      ┌──────────────────────────────────┐
       └─────────────────────►│     ProductVariant              │
                              ├─ product (FK)                   │
                              ├─ sku                            │
                              ├─ price                          │
                              ├─ stock                          │
                              └─ is_active                      │
                              └──────────────────────────────────┘
```

### ۲. User Type Detection

| نوع کاربر | شناسایی | ذخیره سازی |
|----------|---------|-----------|
| **Anonymous** | بدون احراز | `Cart.session_id` |
| **Authenticated** | `request.user.is_authenticated` | `Cart.user` |

---

## مدل‌ها (Models)

### Cart Model

```python
class Cart(models.Model):
    """سبد خرید برای کاربران ناشناس و احراز شده"""
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,  # برای کاربران ناشناس
        related_name='cart'
    )
    session_id = models.CharField(
        max_length=100,
        null=True,  # برای کاربران احراز شده
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Custom Manager
    objects = CartManager()
```

**خصوصیات:**
```python
@property
def total_items(self):
    """تعداد کل اقلام"""
    return sum(item.quantity for item in self.items.all())

@property
def total_price(self):
    """مجموع قیمت تمام اقلام"""
    return sum(item.get_subtotal() for item in self.items.all())

@property
def has_items(self):
    """آیا سبد اقلام دارد"""
    return self.items.exists()
```

**متدها:**
```python
def clear(self):
    """خالی کردن سبد"""
    self.items.all().delete()

def merge_from_session(self, session_key):
    """ادغام اقلام سبد جلسه به سبد کاربر"""
    # هنگام login کاربر فراخوانی می‌شود
```

### CartItem Model

```python
class CartItem(models.Model):
    """اقلام داخل سبد خرید"""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    price_at_add = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="قیمتی که هنگام اضافه کردن ثبت شد"
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'variant')  # تنها یک بار می‌تواند اضافه شود
```

**متدها:**
```python
def get_subtotal(self):
    """قیمت کل (price_at_add * quantity)"""
    return self.price_at_add * self.quantity

def is_in_stock(self):
    """آیا تعداد درخواستی موجود است"""
    return self.variant.stock >= self.quantity
```

### CartManager Custom Methods

```python
class CartManager(models.Manager):
    def get_or_create_for_user(self, user):
        """دریافت یا ایجاد سبد کاربر احراز شده"""
        cart, created = self.get_or_create(user=user)
        return cart
    
    def get_or_create_for_session(self, session_key):
        """دریافت یا ایجاد سبد کاربر ناشناس"""
        cart, created = self.get_or_create(
            session_id=session_key,
            user=None
        )
        return cart
```

---

## Serializers

### CartItemSerializer
نمایش و اعتبارسنجی اقلام سبد

```python
class CartItemSerializer(serializers.ModelSerializer):
    # Read-only nested variant
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        write_only=True
    )
    
    # Computed fields
    subtotal = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='variant.product.name', read_only=True)
    product_sku = serializers.CharField(source='variant.sku', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'variant_id', 'quantity', 'subtotal', 
                  'is_in_stock', 'product_name', 'product_sku']
```

### AddToCartSerializer
اعتبارسنجی ورودی برای اضافه کردن به سبد

```python
class AddToCartSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=1000)
    
    def validate(self, data):
        # اعتبارسنجی variant موجود است
        # اعتبارسنجی موجودی کافی است
        return data
```

### CheckoutSessionSerializer
پاسخ ایجاد جلسه checkout

```python
class CheckoutSessionSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    checkout_url = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    items_count = serializers.IntegerField()
```

---

## ViewSet و Endpoints

### CartViewSet

```python
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAnonymousOrAuthenticated]
```

### 📍 Endpoints

#### 1️⃣ GET /api/cart/
**دریافت سبد خرید فعلی**

**درخواست:**
```bash
curl -X GET http://localhost:8000/api/cart/
```

**پاسخ:**
```json
{
    "id": 1,
    "user_id": null,
    "session_id": "abc123...",
    "items": [
        {
            "id": 5,
            "variant": {
                "id": 10,
                "sku": "TSHIRT-RED-S",
                "name": "Red - Size S",
                "price": "19.99",
                "stock": 10
            },
            "quantity": 2,
            "subtotal": "39.98",
            "is_in_stock": true,
            "product_name": "Test T-Shirt",
            "product_sku": "TSHIRT-RED-S"
        }
    ],
    "total_items": 2,
    "total_price": "39.98",
    "has_items": true,
    "created_at": "2025-02-04T10:00:00Z",
    "updated_at": "2025-02-04T10:05:00Z"
}
```

---

#### 2️⃣ POST /api/cart/add/
**اضافه کردن آیتم به سبد**

**درخواست:**
```json
{
    "variant_id": 10,
    "quantity": 2
}
```

**کمان cURL:**
```bash
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Content-Type: application/json" \
  -d '{"variant_id": 10, "quantity": 2}'
```

**پاسخ موفق (201):**
```json
{
    "message": "Added 2 TSHIRT-RED-S to cart",
    "cart": {
        "id": 1,
        "items": [...],
        "total_items": 2,
        "total_price": "39.98"
    }
}
```

**پاسخ خطا (400) - موجودی کافی نیست:**
```json
{
    "error": "Insufficient stock. Available: 5, Requested: 10",
    "available_stock": 5
}
```

---

#### 3️⃣ PATCH /api/cart/items/{id}/
**تغییر تعداد آیتم**

**درخواست:**
```json
{
    "quantity": 5
}
```

**کمان cURL:**
```bash
curl -X PATCH http://localhost:8000/api/cart/items/5/ \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
```

**پاسخ:**
```json
{
    "id": 1,
    "items": [
        {
            "id": 5,
            "quantity": 5,
            "subtotal": "99.95"
        }
    ],
    "total_price": "99.95"
}
```

---

#### 4️⃣ DELETE /api/cart/items/{id}/
**حذف آیتم از سبد**

**کمان cURL:**
```bash
curl -X DELETE http://localhost:8000/api/cart/items/5/
```

**پاسخ:**
```json
{
    "message": "Removed TSHIRT-RED-S from cart",
    "cart": {
        "id": 1,
        "items": [],
        "total_items": 0,
        "total_price": "0.00"
    }
}
```

---

#### 5️⃣ DELETE /api/cart/
**خالی کردن کل سبد**

**کمان cURL:**
```bash
curl -X DELETE http://localhost:8000/api/cart/
```

**پاسخ:**
```json
{
    "message": "Cleared 3 items from cart",
    "cart": {
        "id": 1,
        "items": [],
        "total_items": 0,
        "total_price": "0.00",
        "has_items": false
    }
}
```

---

#### 6️⃣ POST /api/cart/checkout/
**ایجاد جلسه checkout برای پرداخت**

**درخواست:**
```bash
curl -X POST http://localhost:8000/api/cart/checkout/
```

**پاسخ موفق (201):**
```json
{
    "message": "Checkout session created successfully",
    "checkout": {
        "session_id": "550e8400-e29b-41d4-a716-446655440000",
        "checkout_url": "https://checkout.example.com/session/550e8400-e29b-41d4-a716-446655440000",
        "total_amount": 150.00,
        "items_count": 3
    }
}
```

**پاسخ خطا (400) - سبد خالی:**
```json
{
    "error": "Cannot checkout with empty cart"
}
```

**پاسخ خطا (400) - موجودی تغییر یافته:**
```json
{
    "error": "Some items are no longer in stock",
    "out_of_stock": [
        {
            "sku": "TSHIRT-BLUE-M",
            "requested": 5,
            "available": 2
        }
    ]
}
```

---

## آزمایش API

### ۱. راه‌اندازی سرور

```bash
cd d:\Coding\projects\E-commerxe\proshop
python manage.py runserver 0.0.0.0:8000
```

### ۲. اجرای تست‌ها

```bash
python run_cart_tests.py
```

**تست‌های شامل شده:**
- ✅ سبد کاربران ناشناس
- ✅ اعتبارسنجی موجودی
- ✅ سبد کاربران احراز شده
- ✅ Merge Logic

---

## مثال‌های استفاده

### Python Requests

```python
import requests
import json

BASE_URL = 'http://localhost:8000/api/cart'
headers = {'Content-Type': 'application/json'}

# 1. دریافت سبد
response = requests.get(f'{BASE_URL}/')
cart = response.json()

# 2. اضافه کردن
data = {'variant_id': 10, 'quantity': 2}
response = requests.post(f'{BASE_URL}/add/', json=data)

# 3. تغییر تعداد
data = {'quantity': 5}
response = requests.patch(f'{BASE_URL}/items/5/', json=data)

# 4. حذف
response = requests.delete(f'{BASE_URL}/items/5/')

# 5. Checkout
response = requests.post(f'{BASE_URL}/checkout/')
checkout = response.json()
print(f"Checkout URL: {checkout['checkout']['checkout_url']}")
```

### JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://localhost:8000/api/cart';

// دریافت سبد
async function getCart() {
    const response = await fetch(`${BASE_URL}/`);
    return await response.json();
}

// اضافه کردن
async function addToCart(variantId, quantity) {
    const response = await fetch(`${BASE_URL}/add/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ variant_id: variantId, quantity })
    });
    return await response.json();
}

// تغییر
async function updateCartItem(itemId, quantity) {
    const response = await fetch(`${BASE_URL}/items/${itemId}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity })
    });
    return await response.json();
}

// حذف
async function removeItem(itemId) {
    const response = await fetch(`${BASE_URL}/items/${itemId}/`, {
        method: 'DELETE'
    });
    return await response.json();
}

// Checkout
async function checkout() {
    const response = await fetch(`${BASE_URL}/checkout/`, {
        method: 'POST'
    });
    return await response.json();
}
```

---

## پیاده‌سازی Merge Logic

### تحتیم کاربر Merge

هنگام login، آیتم‌های سبد جلسه کاربر ناشناس به سبد کاربر احراز شده ادغام می‌شوند.

#### راه‌اندازی Merge

**روش 1: Django Signal**

```python
# apps/cart/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """Merge session cart to user cart on login"""
    if not request.session.session_key:
        return
    
    session_key = request.session.session_key
    user_cart = Cart.objects.get_or_create_for_user(user)
    user_cart.merge_from_session(session_key)
```

**ثبت Signal:**

```python
# apps/cart/apps.py
from django.apps import AppConfig

class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'
    
    def ready(self):
        import apps.cart.signals
```

#### Merge Logic توضیح

```python
def merge_from_session(self, session_key):
    """
    Merge items from session cart to user cart
    
    مثال:
    - Session cart: [Item A x2, Item B x1]
    - User cart: [Item A x1]
    - بعد از Merge: [Item A x3, Item B x1]
    """
    if not self.user or not session_key:
        return
    
    try:
        session_cart = Cart.objects.get(session_id=session_key, user=None)
        for item in session_cart.items.all():
            # اگر آیتم در سبد کاربر وجود دارد
            cart_item, created = CartItem.objects.get_or_create(
                cart=self,
                variant=item.variant,
                defaults={
                    'quantity': item.quantity,
                    'price_at_add': item.price_at_add,
                }
            )
            if not created:
                # آیتم موجود، تعداد را اضافه کنید
                cart_item.quantity += item.quantity
                cart_item.save()
        
        # حذف سبد جلسه
        session_cart.delete()
    except Cart.DoesNotExist:
        pass
```

---

## خصوصیات امنیتی

### 1. اعتبارسنجی موجودی

```python
# در AddToCartSerializer
if quantity > variant.stock:
    raise ValidationError(
        f'Insufficient stock. Available: {variant.stock}'
    )
```

### 2. Transaction Safety

```python
# در add_to_cart method
with transaction.atomic():
    cart_item, created = CartItem.objects.get_or_create(...)
    # تمام عملیات داخل یک transaction
```

### 3. Unique Constraint

```python
class Meta:
    unique_together = ('cart', 'variant')
    # فقط یک آیتم از هر variant در سبد
```

### 4. Price Capture

```python
price_at_add = models.DecimalField(...)
# قیمت ثابت شده در زمان اضافه کردن
```

---

## خروجی نمونه API

### GET /api/cart/ (authenticated user)

```json
{
    "id": 5,
    "user_id": 1,
    "session_id": null,
    "items": [
        {
            "id": 12,
            "variant": {
                "id": 3,
                "sku": "TSHIRT-BLUE-M",
                "name": "Blue - Size M",
                "price": "19.99",
                "product": {
                    "id": 1,
                    "name": "Premium T-Shirt",
                    "category": "Clothing"
                }
            },
            "quantity": 2,
            "subtotal": "39.98",
            "is_in_stock": true,
            "product_name": "Premium T-Shirt",
            "product_sku": "TSHIRT-BLUE-M",
            "added_at": "2025-02-04T10:30:00Z",
            "updated_at": "2025-02-04T10:35:00Z"
        },
        {
            "id": 13,
            "variant": {
                "id": 4,
                "sku": "TSHIRT-GREEN-L",
                "name": "Green - Size L",
                "price": "19.99"
            },
            "quantity": 1,
            "subtotal": "19.99",
            "is_in_stock": true,
            "product_name": "Premium T-Shirt",
            "product_sku": "TSHIRT-GREEN-L"
        }
    ],
    "total_items": 3,
    "total_price": "59.97",
    "has_items": true,
    "created_at": "2025-02-04T10:00:00Z",
    "updated_at": "2025-02-04T10:35:00Z"
}
```

---

## نتیجه

✅ **Cart API کامل** برای:
- کاربران ناشناس و احراز شده
- اعتبارسنجی موجودی
- محاسبات خودکار
- Merge logic
- Checkout session

🚀 **آماده برای Step 6**: Payment Processing Integration

---

## فایل‌های مرتبط

```
apps/cart/
├── models.py          # Cart, CartItem
├── serializers.py     # 5 Serializer classes
├── views.py           # CartViewSet
├── urls.py            # API routing
└── migrations/        # Database migrations

proshop/
├── urls.py            # Include cart URLs
└── settings.py        # INSTALLED_APPS

tests/
├── run_cart_tests.py  # Comprehensive tests
└── setup_test_data.py # Test data setup
```

---

**نوشته شده**: 2025-02-04  
**نسخه API**: 1.0  
**Django**: 4.2.10  
**DRF**: 3.15.0
