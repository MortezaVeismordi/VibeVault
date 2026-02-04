# Deployment Guide - VibeVault E-Commerce

This guide will help you deploy the VibeVault Django application to production environments like Railway, Heroku, or any other hosting platform.

## 🚨 Quick Fix for "Set the DB_NAME environment variable" Error

If you're seeing the error `django.core.exceptions.ImproperlyConfigured: Set the DB_NAME environment variable`, you need to configure your database environment variables.

### Solution 1: Use DATABASE_URL (Recommended)

The easiest way is to set a single `DATABASE_URL` environment variable:

```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**Example:**
```bash
DATABASE_URL=postgresql://postgres:mypassword@db.railway.internal:5432/vibevault_db
```

### Solution 2: Use Individual Database Variables

Alternatively, set these individual environment variables:

```bash
DB_NAME=vibevault_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=your_db_host
DB_PORT=5432
```

## 📋 Required Environment Variables

### Minimal Configuration (Required)

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-change-this
DJANGO_SETTINGS_MODULE=proshop.settings.production
ALLOWED_HOSTS=your-domain.com,*.railway.app

# Database (Choose ONE option)
# Option 1: Single DATABASE_URL
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Option 2: Individual settings
# DB_NAME=vibevault_db
# DB_USER=postgres
# DB_PASSWORD=secure_password
# DB_HOST=localhost
# DB_PORT=5432
```

### Optional Configuration

```bash
# Email (for password reset, notifications, etc.)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Cache (for better performance)
REDIS_URL=redis://localhost:6379/1

# Stripe Payment Integration
STRIPE_PUBLIC_KEY=pk_live_your_key
STRIPE_SECRET_KEY=sk_live_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret

# Frontend URL
FRONTEND_URL=https://your-frontend.com

# Error Tracking (Optional)
SENTRY_DSN=https://your-sentry-dsn
```

## 🚀 Deployment Steps

### For Railway.app

1. **Create a new project** on Railway
2. **Add PostgreSQL** service to your project
3. **Set environment variables:**
   - Go to your service settings
   - Add variables tab
   - Copy `DATABASE_URL` from PostgreSQL service
   - Add other required variables:

```bash
SECRET_KEY=django-insecure-$(openssl rand -base64 32)
DJANGO_SETTINGS_MODULE=proshop.settings.production
ALLOWED_HOSTS=${{ RAILWAY_PUBLIC_DOMAIN }},*.railway.app
```

4. **Deploy:**
   - Connect your GitHub repository
   - Railway will automatically detect the Dockerfile
   - Deploy!

### For Heroku

1. **Create a Heroku app:**
```bash
heroku create your-app-name
```

2. **Add PostgreSQL addon:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3. **Set environment variables:**
```bash
heroku config:set SECRET_KEY=$(openssl rand -base64 32)
heroku config:set DJANGO_SETTINGS_MODULE=proshop.settings.production
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

4. **Deploy:**
```bash
git push heroku main
```

### For Generic VPS/Server

1. **Clone repository:**
```bash
git clone https://github.com/yourusername/vibevault.git
cd vibevault
```

2. **Create `.env` file:**
```bash
cp .env.example .env
# Edit .env with your values
nano .env
```

3. **Build and run with Docker:**
```bash
cd proshop
docker build -t vibevault .
docker run -d -p 8000:8000 --env-file ../.env vibevault
```

## 🔧 Troubleshooting

### Error: "Set the DB_NAME environment variable"
**Solution:** Set either `DATABASE_URL` or all individual `DB_*` variables as shown above.

### Error: "Worker failed to boot"
**Solution:** Check that your database is accessible and credentials are correct:
```bash
# Test database connection
psql $DATABASE_URL
```

### Error: "No module named 'apps.accounts'"
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements/production.txt
```

### Static files not loading
**Solution:** Collect static files:
```bash
python manage.py collectstatic --noinput
```

## 📦 Build Process

The application uses the following build process:

1. **Install dependencies** from `requirements/production.txt`
2. **Run migrations:** `python manage.py migrate`
3. **Collect static files:** `python manage.py collectstatic`
4. **Create superuser** (if needed)
5. **Start Gunicorn** server

This is all handled by the `entrypoint.sh` script.

## 🔐 Security Checklist

- [ ] Change `SECRET_KEY` to a random string
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use HTTPS (SSL/TLS)
- [ ] Set secure database password
- [ ] Enable Redis for caching (recommended)
- [ ] Configure Sentry for error tracking
- [ ] Set up proper backup strategy

## 📞 Support

If you encounter any issues during deployment:

1. Check the logs: `heroku logs --tail` or equivalent for your platform
2. Verify all environment variables are set correctly
3. Make sure the database is accessible
4. Check the [GitHub Issues](https://github.com/yourusername/vibevault/issues)

## 🎉 Post-Deployment

After successful deployment:

1. **Create a superuser:**
```bash
python manage.py createsuperuser
```

2. **Access admin panel:**
```
https://your-domain.com/admin
```

3. **Test the API:**
```
https://your-domain.com/api/schema/swagger-ui/
```

Good luck with your deployment! 🚀
