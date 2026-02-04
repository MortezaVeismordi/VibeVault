# Proshop - E-Commerce Platform with Stripe Integration

![Django](https://img.shields.io/badge/Django-4.2.10-green) ![DRF](https://img.shields.io/badge/DRF-3.15.0-blue) ![Stripe](https://img.shields.io/badge/Stripe-Integrated-purple) ![License](https://img.shields.io/badge/License-MIT-blue)

A modern, production-ready e-commerce platform built with **Django 4.2 LTS** and **Django REST Framework**. Features complete payment processing with **Stripe**, inventory management, order tracking, and email notifications.

**🚀 Live Demo:** Coming Soon  
**📘 Documentation:** [docs/](docs/)  
**💼 Portfolio:** [Your Portfolio Link]

---

## ✨ Key Features

### E-Commerce Core
- ✅ **Product Catalog** - Categories, products, and variants with attributes
- ✅ **Advanced Search** - Filter by price, category, brand, rating
- ✅ **Shopping Cart** - Session and user-based cart management with merge logic
- ✅ **Inventory Management** - Real-time stock tracking and updates
- ✅ **Order Management** - Order history, status tracking, cancellation
- ✅ **Reviews & Ratings** - Customer reviews with rating system

### Payment Processing
- ✅ **Stripe Checkout** - Secure payment processing with Stripe
- ✅ **Webhook Handling** - Event-driven order updates on payment success/failure
- ✅ **Payment Tracking** - Full audit trail with Stripe integration IDs
- ✅ **Security** - Webhook signature verification, CSRF protection
- ✅ **Test Mode** - Full test card support for development

### User Experience
- ✅ **User Accounts** - Registration, login, profile management
- ✅ **Email Notifications** - Order confirmation, payment status, shipping updates
- ✅ **REST API** - Complete API for frontend integration
- ✅ **DRF Browsable API** - Interactive API documentation
- ✅ **Admin Interface** - Django admin with custom views

### Performance & Security
- ✅ **Database Indexes** - Optimized queries on high-traffic tables
- ✅ **CORS Enabled** - Frontend integration ready
- ✅ **Environment Secrets** - Secure key management with .env
- ✅ **Error Handling** - Comprehensive error responses
- ✅ **Logging** - Full audit trail for debugging

---

## 🏗️ Tech Stack

### Backend
- **Django 4.2.10 LTS** - Web framework
- **Django REST Framework 3.15.0** - API framework
- **SQLite (dev) / PostgreSQL (prod)** - Database
- **Stripe Python SDK v10.0.0** - Payment processing

### Frontend (Ready for Integration)
- **HTML/CSS/JavaScript** - Base templates
- **Bootstrap/Tailwind** - Styling (via templates)
- **Fetch API** - API communication

### DevOps & Tools
- **Git** - Version control
- **Docker** (optional) - Containerization
- **Railway/Render** - Deployment ready

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip / pipenv
- Git
- Stripe Account (for payment testing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/proshop.git
cd proshop
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements/base.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your Stripe keys
```

5. **Run migrations**
```bash
cd proshop
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load sample data** (optional)
```bash
python manage.py loaddata fixtures/products.json
```

8. **Run development server**
```bash
python manage.py runserver
```

Access at: `http://localhost:8000`  
Admin: `http://localhost:8000/admin`

---

## 📡 API Documentation

### Authentication
All protected endpoints require user authentication.

### Core Endpoints

#### Products
```
GET    /api/shop/products/              - List products (paginated)
GET    /api/shop/products/{id}/         - Get product detail
GET    /api/shop/products/{id}/variants/ - Get product variants
GET    /api/shop/categories/            - List categories
```

#### Shopping Cart
```
GET    /api/cart/                       - Get cart items
POST   /api/cart/add/                   - Add item to cart
PUT    /api/cart/update/{id}/           - Update cart item quantity
DELETE /api/cart/remove/{id}/           - Remove item from cart
POST   /api/cart/clear/                 - Clear entire cart
```

#### Orders
```
GET    /api/orders/                     - Get user's orders (auth required)
GET    /api/orders/{id}/                - Get order detail (auth required)
GET    /api/orders/number/{order_number}/ - Get order by number (auth required)
POST   /api/orders/{id}/cancel/         - Cancel order (auth required)
```

#### Payment
```
POST   /api/payment/checkout/           - Create Stripe session
POST   /api/payment/webhook/            - Stripe webhook endpoint
GET    /api/payment/status/?session_id=...  - Check payment status
```

### Response Formats

**Success (200/201):**
```json
{
  "id": 1,
  "name": "Product Name",
  "price": 99.99,
  ...
}
```

**Error (400/500):**
```json
{
  "error": "Detailed error message",
  "field_errors": {
    "field_name": ["Error 1", "Error 2"]
  }
}
```

---

## 💳 Payment Testing

### Stripe Test Cards

**Success:** `4242 4242 4242 4242`
- Expiry: Any future date
- CVC: Any 3 digits
- Result: Payment succeeds

**Declined:** `4000 0000 0000 0002`
- Expiry: Any future date
- CVC: Any 3 digits
- Result: Payment declined

**Requires Auth:** `4000 0000 0000 3220`
- Requires 3D Secure authentication
- Uses test credentials

### Testing Webhooks Locally

1. **Install Stripe CLI**
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Other systems: https://stripe.com/docs/stripe-cli
```

2. **Forward webhooks**
```bash
stripe listen --forward-to localhost:8000/api/payment/webhook/
```

3. **Get webhook signing secret**
```bash
# Copy the whsec_... value from CLI output and add to .env
STRIPE_WEBHOOK_SECRET=whsec_test_...
```

4. **Complete test payment**
- Run checkout flow with test card `4242 4242 4242 4242`
- Stripe CLI will show incoming webhook events
- Check database to verify Order/Payment updates

---

## 📊 Project Structure

```
proshop/
├── apps/
│   ├── shop/              - Product catalog
│   │   ├── models.py      - Product, Category, Variant
│   │   ├── views.py       - Product viewsets
│   │   └── urls.py        - API routes
│   ├── cart/              - Shopping cart
│   │   ├── models.py      - Cart, CartItem
│   │   ├── views.py       - Cart API views
│   │   └── urls.py        - Cart routes
│   ├── orders/            - Order management
│   │   ├── models.py      - Order, OrderItem
│   │   ├── api_views.py   - Order API endpoints
│   │   ├── signals.py     - Email notifications
│   │   └── urls.py        - Order routes
│   ├── payment/           - Stripe integration
│   │   ├── models.py      - Payment, PaymentLog
│   │   ├── views.py       - Checkout, Webhook, Status
│   │   ├── serializers.py - Payment serializers
│   │   └── urls.py        - Payment routes
│   ├── accounts/          - User management
│   │   ├── models.py      - CustomUser
│   │   └── views.py       - Auth views
│   └── reviews/           - Reviews & ratings
│       ├── models.py      - Review model
│       └── views.py       - Review endpoints
├── proshop/
│   ├── settings/
│   │   ├── base.py        - Base settings
│   │   ├── development.py - Dev settings
│   │   └── production.py  - Prod settings
│   ├── urls.py            - Main URL config
│   └── wsgi.py            - WSGI config
├── .env                   - Environment variables
├── manage.py              - Django CLI
└── requirements/
    ├── base.txt           - Core dependencies
    ├── dev.txt            - Development tools
    └── prod.txt           - Production tools
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Django
DJANGO_ENV=development
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.sqlite3  # or postgresql
DB_NAME=db.sqlite3

# Stripe (Get from https://dashboard.stripe.com/apikeys)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### Database Selection

**Development (SQLite):**
```python
# Default in development.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

**Production (PostgreSQL):**
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='postgresql://...')
}
```

---

## 📈 Database Schema Highlights

### Key Indexes for Performance
- `Product.slug` - Product lookup
- `Order.user_id` - User's order history
- `Payment.stripe_session_id` - Webhook lookup
- `Cart.user_id` / `Cart.session_id` - Cart retrieval
- `OrderItem.order_id` - Order items

### Data Relationships
```
Product (1) -----> (Many) ProductVariant
           -----> (Many) Review
           
Order (1) -----> (Many) OrderItem -----> ProductVariant
      -----> (1) Payment -----> (Many) PaymentLog

Cart (1) -----> (Many) CartItem -----> ProductVariant

User (1) -----> (Many) Order
    -----> (Many) Review
    -----> (Many) Cart
```

---

## 🧪 Testing

### Manual Testing Checklist

**Cart Flow:**
- [ ] Add items to cart (anonymous)
- [ ] Update quantities
- [ ] Remove items
- [ ] Merge carts on login
- [ ] Clear cart

**Checkout Flow:**
- [ ] View cart total
- [ ] Create checkout session
- [ ] Redirect to Stripe
- [ ] Complete payment with test card
- [ ] Verify order created
- [ ] Check stock reduced
- [ ] Verify email sent

**Order Management:**
- [ ] View order history
- [ ] Get order details
- [ ] See order items
- [ ] Cancel pending order
- [ ] Check payment status

### Integration Testing
```bash
# Run tests
python manage.py test

# With coverage
coverage run --source='apps' manage.py test
coverage report
```

---

## 🚀 Deployment

### Option 1: Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Deploy
railway up
```

### Option 2: Render.com

1. Connect GitHub repository
2. Create new Web Service
3. Set environment variables
4. Deploy!

### Pre-Deployment Checklist
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use production Stripe keys
- [ ] Configure PostgreSQL
- [ ] Setup email (SendGrid/Gmail)
- [ ] Configure static files (WhiteNoise)
- [ ] Setup error monitoring (Sentry)
- [ ] Add HTTPS certificate
- [ ] Configure backups

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Python SDK](https://github.com/stripe/stripe-python)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 💬 Support

For support, email support@proshop.com or open an issue on GitHub.

---

## 🎯 Roadmap

- [ ] Frontend React/Vue integration
- [ ] Advanced analytics dashboard
- [ ] Wishlist functionality
- [ ] Product recommendations (ML)
- [ ] Multi-currency support
- [ ] Affiliate program
- [ ] Mobile app (React Native)
- [ ] Inventory forecasting

---

**Built with ❤️ by [Your Name]**

Last updated: February 4, 2026
