from django.urls import path
from .views import CheckoutView, WebhookView, PaymentStatusView
from .page_views import OrderSuccessView, OrderCancelView

urlpatterns = [
    # Stripe API endpoints
    path('checkout/', CheckoutView.as_view(), name='stripe_checkout'),
    path('webhook/', WebhookView.as_view(), name='stripe_webhook'),
    path('status/', PaymentStatusView.as_view(), name='payment_status'),
    
    # Success/Cancel pages
    path('success/', OrderSuccessView.as_view(), name='order_success'),
    path('cancel/', OrderCancelView.as_view(), name='order_cancel'),
]
