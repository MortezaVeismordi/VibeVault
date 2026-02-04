"""
Base Django settings - shared across all environments
This file contains all common settings.
Environment-specific overrides are in development.py, production.py, etc.
"""
import os
from pathlib import Path
import environ
import dj_database_url

# Initialize environment
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read environment variables from .env file
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(str(env_file))

# ===========================
# SECURITY SETTINGS
# ===========================
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# ===========================
# APPLICATION DEFINITION
# ===========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proshop.wsgi.application'

# ===========================
# DATABASE CONFIGURATION
# ===========================
# Support DATABASE_URL env variable for easy Docker/Heroku deployment
DATABASE_URL = env('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to individual database settings
    DATABASES = {
        'default': {
            'ENGINE': env('DB_ENGINE', default='django.db.backends.sqlite3'),
            'NAME': env('DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
            'USER': env('DB_USER', default=''),
            'PASSWORD': env('DB_PASSWORD', default=''),
            'HOST': env('DB_HOST', default=''),
            'PORT': env('DB_PORT', default=''),
        }
    }

# ===========================
# PASSWORD VALIDATION
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ===========================
# INTERNATIONALIZATION
# ===========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===========================
# STATIC FILES & MEDIA
# ===========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===========================
# DEFAULT PRIMARY KEY FIELD
# ===========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================
# CUSTOM USER MODEL
# ===========================
AUTH_USER_MODEL = 'accounts.CustomUser'

# ===========================
# SESSION CONFIGURATION
# ===========================
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ===========================
# AUTHENTICATION
# ===========================
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'shop'
LOGOUT_REDIRECT_URL = 'shop'

# ===========================
# REST FRAMEWORK
# ===========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ===========================
# DRF-SPECTACULAR (SWAGGER/OPENAPI)
# ===========================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Proshop E-Commerce API',
    'DESCRIPTION': 'Complete REST API for Proshop e-commerce platform with Stripe integration',
    'VERSION': '1.0.0',
    'SERVERS': [
        {
            'url': 'http://localhost:8000',
            'description': 'Development server',
        },
    ],
    'CONTACT': {
        'name': 'Proshop Support',
        'email': 'support@proshop.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'SCHEMA_PATH_PREFIX': r'/api/',
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayOperationId': True,
    },
}

# ===========================
# CORS CONFIGURATION
# ===========================
CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=[
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]
)
CORS_ALLOW_CREDENTIALS = True

# ===========================
# CACHING
# ===========================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'proshop-cache',
    }
}

# ===========================
# LOGGING
# ===========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ===========================
# EMAIL CONFIGURATION
# ===========================
EMAIL_BACKEND = env(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@proshop.com')

# ===========================
# STRIPE PAYMENT CONFIGURATION
# ===========================
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET', default='')

# Frontend URL for Stripe redirect (for checkout success/cancel)
FRONTEND_URL = env('FRONTEND_URL', default='http://localhost:3000')

# ===========================
# AWS S3 (OPTIONAL)
# ===========================
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')

# ===========================
# LOCAL APPS
# ===========================
LOCAL_APPS = [
    'apps.accounts.apps.AccountsConfig',
    'apps.shop.apps.ShopConfig',
    'apps.cart.apps.CartConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.payment.apps.PaymentConfig',
    'apps.reviews.apps.ReviewsConfig',
]

INSTALLED_APPS += LOCAL_APPS

