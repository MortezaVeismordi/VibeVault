"""
URL Configuration for proshop project
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # API Documentation (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API URLs
    path('api/', include('apps.shop.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/payment/', include('apps.payment.urls')),
    
    # Legacy URLs
    path('accounts/', include('apps.accounts.urls')),
    path('shop/', include('apps.shop.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('payment/', include('apps.payment.urls')),
    path('reviews/', include('apps.reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [
            path('__debug__/', include('debug_toolbar.urls')),
        ]
else:
    # Serve React frontend in production
    urlpatterns += [
        path('', TemplateView.as_view(template_name='index.html'), name='index'),
        path('<path:url>', TemplateView.as_view(template_name='index.html'), name='index-fallback'),
    ]
