# Proshop E-Commerce API - Quick Reference Guide

## 🚀 Startup

```bash
cd proshop
python manage.py runserver
```

Server runs at: http://localhost:8000

---

## 📚 API Documentation

### Interactive Documentation (Try-it-out)
- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **Raw Schema:** http://localhost:8000/api/schema/

---

## 🛒 Key Endpoints

### Shop / Products
```
GET    /api/shop/products/              # List all products
GET    /api/shop/products/{id}/         # Get product details
GET    /api/shop/categories/            # List categories
GET    /api/shop/categories/{id}/       # Get category details
```

### Shopping Cart
```
GET    /api/cart/                       # Get cart (session-based)
POST   /api/cart/                       # Add to cart
PUT    /api/cart/{item_id}/             # Update cart item
DELETE /api/cart/{item_id}/             # Remove from cart
POST   /api/cart/clear/                 # Clear entire cart
```

### Payment / Orders
```
POST   /api/payment/checkout/           # Create checkout session (Stripe)
POST   /api/payment/webhook/            # Stripe webhook (auto-called)
GET    /api/payment/status/{session_id}/ # Check payment status
GET    /api/payment/success/            # Success page (after payment)
GET    /api/payment/cancel/             # Cancel page (if payment cancelled)
```

### Order History
```
GET    /api/orders/                     # Get user's orders (requires auth)
GET    /api/orders/{id}/                # Get order details
```

### Reviews
```
GET    /api/reviews/                    # List all reviews
POST   /api/reviews/                    # Create review (requires auth)
GET    /api/reviews/{id}/               # Get review details
PUT    /api/reviews/{id}/               # Update review (owner only)
DELETE /api/reviews/{id}/               # Delete review (owner only)
```

### Authentication
```
POST   /api-auth/login/                 # Login (session-based)
POST   /accounts/register/              # Register new account
```

---

## 🔧 Management Commands

### Create Sample Data
```bash
# Create fresh sample data
python manage.py create_sample_data

# Clear and recreate
python manage.py create_sample_data --clear

# Test account created:
# Username: customer1
# Email: customer1@example.com
# Password: password123
```

### Database
```bash
python manage.py migrate              # Apply migrations
python manage.py makemigrations       # Create migrations
python manage.py createsuperuser      # Create admin user
```

### System Checks
```bash
python manage.py check                # Check configuration
python manage.py check --deploy       # Production checks
```

---

## 💳 Payment Flow

1. **Add items to cart**
   ```
   POST /api/cart/
   Body: {"product_id": 1, "quantity": 2}
   ```

2. **Create checkout session**
   ```
   POST /api/payment/checkout/
   Body: {"cart_items": [...]}
   Response: {"checkout_url": "https://stripe.com/..."}
   ```

3. **Redirect to Stripe** → User completes payment

4. **Webhook notification** (auto)
   - Stripe sends webhook to /api/payment/webhook/
   - Order created/updated automatically

5. **Check status**
   ```
   GET /api/payment/status/{session_id}/
   ```

6. **Success page**
   ```
   GET /api/payment/success/?order_id={order_id}
   ```

---

## 📦 Sample Data Included

### Users
- customer1 / password123
- customer2 / password123
- customer3 / password123

### Products (10 total)
- Wireless Bluetooth Headphones ($79.99)
- 4K Webcam ($149.99)
- USB-C Cable Pack ($24.99)
- Cotton T-Shirt ($29.99)
- Denim Jeans ($59.99)
- Non-Stick Cookware Set ($89.99)
- Stainless Steel Kettle ($34.99)
- Yoga Mat ($49.99)
- Dumbbell Set ($129.99)
- Python Programming Book ($44.99)

### Categories
- Electronics
- Clothing
- Home & Kitchen
- Sports
- Books

---

## 🛡️ Security Settings

### Development (`proshop/settings/development.py`)
- DEBUG = True
- localhost allowed
- SQLite database
- Django Debug Toolbar enabled

### Production (`proshop/settings/production.py`)
- DEBUG = False
- HTTPS required
- Secure cookies
- HSTS enabled
- PostgreSQL recommended
- Environment variables for secrets

**To use production settings:**
```bash
export DJANGO_SETTINGS_MODULE=proshop.settings.production
python manage.py runserver
```

---

## 🔐 Environment Variables (Required for Production)

```bash
# Django
DEBUG=False
SECRET_KEY=your-secure-key
DJANGO_SETTINGS_MODULE=proshop.settings.production

# Database
DATABASE_URL=postgresql://user:pass@localhost/proshop

# Stripe (get from https://dashboard.stripe.com/)
STRIPE_LIVE_PUBLIC_KEY=pk_live_...
STRIPE_LIVE_SECRET_KEY=sk_live_...

# Email (optional, for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Allowed hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## 📊 Admin Panel

Access at: http://localhost:8000/admin/

**Superuser setup:**
```bash
python manage.py createsuperuser
```

**Manage:**
- Products and categories
- Orders and order items
- Users and reviews
- Payment records

---

## 🧪 Testing with cURL

### List Products
```bash
curl http://localhost:8000/api/shop/products/
```

### Add to Cart
```bash
curl -X POST http://localhost:8000/api/cart/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Get Cart
```bash
curl http://localhost:8000/api/cart/
```

### Create Order (with payment)
```bash
curl -X POST http://localhost:8000/api/payment/checkout/ \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product": 1, "quantity": 2}]}'
```

---

## 📝 Project Structure

```
proshop/
├── proshop/                          # Project settings
│   ├── settings/
│   │   ├── base.py                  # Common settings
│   │   ├── development.py           # Dev settings
│   │   └── production.py            # Prod settings
│   ├── urls.py                      # Main URL router
│   ├── wsgi.py                      # WSGI config
│   └── asgi.py                      # ASGI config
│
├── apps/
│   ├── shop/                        # Products & categories
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── management/commands/
│   │       └── create_sample_data.py
│   │
│   ├── cart/                        # Shopping cart
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   │
│   ├── payment/                     # Stripe payment
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── page_views.py           # Success/cancel pages
│   │   ├── serializers.py
│   │   ├── webhooks.py
│   │   └── templates/payment/
│   │       ├── success.html
│   │       └── cancel.html
│   │
│   ├── orders/                      # Order management
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   │
│   ├── accounts/                    # User management
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   │
│   └── reviews/                     # Product reviews
│       ├── models.py
│       ├── views.py
│       └── serializers.py
│
├── requirements/
│   ├── base.txt                     # Common dependencies
│   ├── development.txt              # Dev dependencies
│   └── production.txt               # Prod dependencies
│
├── manage.py                        # Django CLI
└── README.md                        # Project docs
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Locked
```bash
rm db.sqlite3
python manage.py migrate
python manage.py create_sample_data
```

### Import Errors
```bash
pip install -r requirements/base.txt
```

### Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
python manage.py migrate
```

---

## 📞 Support

- Check API docs: http://localhost:8000/api/docs/
- View admin: http://localhost:8000/admin/
- Check logs: Terminal output during runserver

---

## 🚀 Ready for Deployment!

The project is now:
- ✅ Feature complete
- ✅ Well documented
- ✅ Secure
- ✅ Ready for production

**Next step:** Push to GitHub and deploy! 🎉

```bash
git add .
git commit -m "feat: Step 7 - Final Polish for Production Deployment"
git push origin main
```

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-04  
**Status:** PRODUCTION READY ✨
