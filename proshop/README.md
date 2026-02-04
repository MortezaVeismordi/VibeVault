# Proshop - E-Commerce Platform

A scalable, production-ready Django e-commerce platform with a modular app architecture. Built with best practices for maintainability and performance.

## 🚀 Features

- **Product Management**: Categories, products, variants, and images
- **User Accounts**: Registration, profiles, authentication
- **Shopping Cart**: Session-based and user-based cart management
- **Orders**: Complete order lifecycle management
- **Payment Processing**: Stripe integration ready
- **Reviews & Ratings**: Product reviews with helpful voting
- **Admin Dashboard**: Full Django admin interface
- **REST API**: Django REST Framework ready
- **Docker Support**: Development and production Docker configurations
- **PostgreSQL**: Robust database backend
- **Redis**: Caching and session management
- **Nginx**: Production-grade web server

## 📋 Tech Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Web Server**: Nginx (production)
- **Task Queue**: Celery (optional)
- **Payment**: Stripe
- **Containerization**: Docker & Docker Compose

## 🏗️ Project Structure

```
proshop/
├── apps/                    # Django applications
│   ├── accounts/           # User management
│   ├── shop/              # Product catalog
│   ├── cart/              # Shopping cart
│   ├── orders/            # Order management
│   ├── payment/           # Payment processing
│   ├── reviews/           # Product reviews
│   └── utils/             # Helpers and utilities
├── proshop/               # Main project config
│   ├── settings/          # Environment-specific settings
│   │   ├── base.py       # Common settings
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/             # Global templates
├── static/                # Global static files
├── media/                 # User-uploaded files
├── requirements/          # Python dependencies
├── docker-compose.yml     # Development container setup
├── docker-compose.prod.yml # Production container setup
├── Dockerfile
├── entrypoint.sh
└── manage.py
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Local Development Setup

1. **Clone the repository**
   ```bash
   cd d:\Coding\projects\E-commerxe\proshop
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements/development.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Visit http://localhost:8000

### Docker Development

1. **Start services**
   ```bash
   docker-compose up -d
   ```

2. **Access the application**
   - Web: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Database: localhost:5432
   - Redis: localhost:6379

3. **Stop services**
   ```bash
   docker-compose down
   ```

### Docker Production

1. **Configure environment**
   ```bash
   cp .env.example .env.prod
   # Edit with production settings
   ```

2. **Build and run**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Access**
   - Web: http://localhost:80

## 📚 API Endpoints

### Authentication
- `POST /accounts/register/` - Register new user
- `POST /accounts/login/` - Login user
- `POST /accounts/logout/` - Logout user

### Shop
- `GET /shop/` - List products
- `GET /shop/product/<slug>/` - Product detail
- `GET /shop/category/<slug>/` - Category products

### Cart
- `GET /cart/` - View cart
- `POST /cart/add/<product_id>/` - Add to cart
- `POST /cart/remove/<item_id>/` - Remove from cart
- `POST /cart/update/<item_id>/` - Update quantity

### Orders
- `GET /orders/` - List user orders
- `GET /orders/<order_id>/` - Order detail
- `POST /orders/<order_id>/cancel/` - Cancel order

### Payments
- `GET /payment/order/<order_id>/` - Payment page
- `POST /payment/<payment_id>/process/` - Process payment

### Reviews
- `POST /reviews/product/<product_id>/add/` - Add review
- `POST /reviews/<review_id>/delete/` - Delete review
- `POST /reviews/<review_id>/helpful/` - Mark as helpful

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=proshop
DB_USER=postgres
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Stripe
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
```

## 📖 Database Models

### Accounts
- `UserProfile` - Extended user information

### Shop
- `Category` - Product categories
- `Product` - Products with pricing
- `ProductVariant` - Product variants (size, color)
- `ProductImage` - Additional product images

### Cart
- `Cart` - Shopping cart
- `CartItem` - Items in cart

### Orders
- `Order` - Customer orders
- `OrderItem` - Items in order

### Payment
- `Payment` - Payment transactions
- `PaymentLog` - Payment attempt logs
- `Refund` - Refund records

### Reviews
- `Review` - Product reviews
- `ReviewImage` - Review images
- `ReviewVote` - Review helpfulness votes

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

With coverage:
```bash
pytest --cov=apps
```

## 🔒 Security

- CSRF protection enabled
- SQL injection prevention
- XSS protection
- Password hashing with PBKDF2
- Secure session management
- HTTPS ready (production)
- Rate limiting ready

## 📦 Deployment

### Gunicorn + Nginx

```bash
# Install production requirements
pip install -r requirements/production.txt

# Run with Gunicorn
gunicorn proshop.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/AmazingFeature`
2. Commit changes: `git commit -m 'Add AmazingFeature'`
3. Push to branch: `git push origin feature/AmazingFeature`
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, email support@proshop.com or open an issue on GitHub.

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- PostgreSQL
- Stripe API
