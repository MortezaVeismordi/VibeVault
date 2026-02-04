"""
URL configuration for cart app API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet


# Create router and register viewsets
router = DefaultRouter()
router.register(r'', CartViewSet, basename='cart')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
