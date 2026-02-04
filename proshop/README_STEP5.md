# E-Commerce API - Step 5: Cart & Checkout Management

## 📦 خلاصه Step 5

**Status**: ✅ **COMPLETE**

مرحله ۵ یک **API کامل برای سبد خرید** (Shopping Cart) و **Checkout** فراهم می‌کند.

---

## 🎯 اهداف تکمیل شده

✅ **Cart Models** - `Cart` و `CartItem` با روابط بهینه  
✅ **Anonymous + Authenticated Support** - پشتیبانی دو نوع کاربر  
✅ **Stock Validation** - اعتبارسنجی موجودی  
✅ **Price Capture** - ثبت قیمت در زمان اضافه کردن  
✅ **CartManager** - مدیریت خودکار سبد کاربران  
✅ **Merge Logic** - ادغام سبد جلسه به سبد کاربر  
✅ **5 Serializers** - تمام نیازهای واسط داده  
✅ **CartViewSet** - 6 Endpoint برای تمام عملیات  
✅ **Comprehensive Testing** - تست کامل تمام عملیات  
✅ **Documentation** - مستندات کامل فارسی و انگلیسی  

---

## 🏗️ معماری

### Database Schema

```
Cart (سبد خرید)
├── id (PK)
├── user (FK → CustomUser) [optional - برای کاربران احراز شده]
├── session_id (CharField) [optional - برای کاربران ناشناس]
├── created_at
└── updated_at

CartItem (آیتم سبد)
├── id (PK)
├── cart (FK → Cart)
├── variant (FK → ProductVariant)
├── quantity
├── price_at_add [قیمت ثابت]
├── added_at
└── updated_at
```

### Custom Manager

```python
Cart.objects.get_or_create_for_user(user)      # کاربر احراز شده
Cart.objects.get_or_create_for_session(key)    # کاربر ناشناس
```

---

## 🔌 API Endpoints

| Method | URL | توضیح |
|--------|-----|-------|
| **GET** | `/api/cart/` | دریافت سبد فعلی |
| **POST** | `/api/cart/add/` | اضافه کردن آیتم |
| **PATCH** | `/api/cart/items/<id>/` | تغییر تعداد |
| **DELETE** | `/api/cart/items/<id>/` | حذف آیتم |
| **DELETE** | `/api/cart/` | خالی کردن سبد |
| **POST** | `/api/cart/checkout/` | ایجاد checkout session |

---

## 📊 مثال‌های استفاده

### 1️⃣ دریافت سبد

```bash
curl -X GET http://localhost:8000/api/cart/
```

**پاسخ:**
```json
{
    "id": 1,
    "items": [
        {
            "id": 5,
            "variant": { "sku": "TSHIRT-RED-S", "price": "19.99" },
            "quantity": 2,
            "subtotal": "39.98",
            "is_in_stock": true
        }
    ],
    "total_items": 2,
    "total_price": "39.98",
    "has_items": true
}
```

### 2️⃣ اضافه کردن

```bash
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Content-Type: application/json" \
  -d '{"variant_id": 10, "quantity": 2}'
```

**پاسخ:**
```json
{
    "message": "Added 2 TSHIRT-RED-S to cart",
    "cart": { ... }
}
```

### 3️⃣ Checkout

```bash
curl -X POST http://localhost:8000/api/cart/checkout/
```

**پاسخ:**
```json
{
    "checkout": {
        "session_id": "550e8400-e29b-41d4...",
        "checkout_url": "https://checkout.example.com/session/...",
        "total_amount": 150.00,
        "items_count": 3
    }
}
```

---

## 🔒 خصوصیات امنیتی

### 1. Stock Validation
```python
if quantity > variant.stock:
    return 400, "Insufficient stock"
```

### 2. Transaction Atomicity
```python
with transaction.atomic():
    # تمام عملیات داخل یک transaction
```

### 3. Unique Constraint
```python
class Meta:
    unique_together = ('cart', 'variant')
    # فقط یک آیتم از variant در سبد
```

### 4. Price Capture
```python
# قیمت زمان اضافه کردن ثبت می‌شود
price_at_add = variant.price
```

---

## 🔄 Merge Logic

هنگام **login** کاربر:

```python
# سبد جلسه: [A×2, B×1]
# سبد کاربر: [A×1]
#
# بعد از merge: [A×3, B×1]
```

**اجرای Merge:**
```python
user_cart.merge_from_session(request.session.session_key)
```

---

## 📂 فایل‌های جدید

```
apps/cart/
├── models.py (155 lines)
│   ├── CartManager
│   ├── Cart
│   └── CartItem
├── serializers.py (168 lines)
│   ├── CartItemSerializer
│   ├── CartSerializer
│   ├── AddToCartSerializer
│   ├── UpdateCartItemSerializer
│   └── CheckoutSessionSerializer
├── views.py (287 lines)
│   └── CartViewSet [6 methods + helpers]
└── urls.py
    └── DefaultRouter configuration
```

---

## 🧪 تست کردن

### آماده‌سازی

```bash
cd d:\Coding\projects\E-commerxe\proshop
python manage.py migrate
```

### اجرای تست‌ها

```bash
python run_cart_tests.py
```

**تست‌های اجرا شده:**
- ✅ Cart operations for anonymous users
- ✅ Stock validation
- ✅ Authenticated user cart
- ✅ Merge logic verification

---

## 📈 نمودار Workflow

```
┌─────────────────────────────────────────────────────────┐
│                   کاربر ناشناس                          │
│  (بدون login - با session_id)                          │
└─────────┬───────────────────────────────────────────────┘
          │
          ├─► GET /api/cart/              → دریافت سبد
          ├─► POST /api/cart/add/         → اضافه کردن
          ├─► PATCH /api/cart/items/<id>/ → تغییر
          ├─► DELETE /api/cart/           → خالی کردن
          └─► POST /api/cart/checkout/    → checkout
          
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│             کاربر login می‌کند                         │
│  merge_from_session(session_key) فراخوانی می‌شود      │
└─────────┬───────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              کاربر احراز شده                            │
│   (با user_id در database)                             │
└─────────┬───────────────────────────────────────────────┘
          │
          ├─► سبد پیشین + سبد جلسه = سبد جدید
          │
          └─► تمام آیتم‌ها حفظ شده‌اند ✓
```

---

## 🚀 اجرای سرور

```bash
cd d:\Coding\projects\E-commerxe\proshop
python manage.py runserver 0.0.0.0:8000
```

سپس:
- **Browsable API**: http://localhost:8000/api/cart/
- **Admin Panel**: http://localhost:8000/admin/

---

## 📝 فایل‌های مستندات

- [STEP5_COMPLETE.md](STEP5_COMPLETE.md) - مستندات جامع فارسی
- [run_cart_tests.py](run_cart_tests.py) - تست‌های کامل
- [setup_test_data.py](setup_test_data.py) - آماده‌سازی داده

---

## 🔗 ارتباط با سایر مراحل

**Step 4** ← API محصولات  
**Step 5** ← **Cart & Checkout** ✓  
**Step 6** ← Payment Processing (بعدی)  

---

## 📊 آمار

- **مدل‌ها**: 2 (Cart, CartItem)
- **Serializers**: 5
- **ViewSet Methods**: 6
- **API Endpoints**: 6
- **Lines of Code**: 610+ lines
- **Tests**: 4 test suites
- **Documentation**: 500+ lines

---

## ✨ ویژگی‌های برجسته

🎯 **User-Session Detection**: خودکار شناسایی کاربر  
🔐 **Stock Validation**: قبل از اضافه کردن  
💾 **Price Capture**: قیمت ثابت شده  
🔄 **Cart Merge**: ادغام خودکار هنگام login  
📦 **Checkout Ready**: آماده برای Payment Integration  
⚡ **Query Optimization**: select_related, prefetch_related  
🧪 **Well Tested**: تست کامل تمام سناریوها  
📖 **Fully Documented**: مستندات کامل  

---

**نوشته شده**: 2025-02-04  
**نسخه**: 1.0  
**وضعیت**: ✅ PRODUCTION READY
