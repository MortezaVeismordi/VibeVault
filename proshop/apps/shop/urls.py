"""
Shop app URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='api-products')
router.register(r'categories', views.CategoryViewSet, basename='api-categories')
router.register(r'variants', views.ProductVariantViewSet, basename='api-variants')

# URL patterns
urlpatterns = [
    # API endpoints (already prefixed with 'api/shop/' in main urls.py)
    path('', include(router.urls)),
    
    # Traditional views (if needed)
    path('shop-list/', views.shop_list, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
]
