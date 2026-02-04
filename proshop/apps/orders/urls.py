from django.urls import path
from . import views
from .api_views import (
    OrderListView,
    OrderDetailView,
    OrderByNumberView,
    OrderCancelView,
)

urlpatterns = [
    # Traditional views
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # API endpoints
    path('api/', OrderListView.as_view(), name='api-order-list'),
    path('api/<int:pk>/', OrderDetailView.as_view(), name='api-order-detail'),
    path('api/number/<str:order_number>/', OrderByNumberView.as_view(), name='api-order-by-number'),
    path('api/<int:pk>/cancel/', OrderCancelView.as_view(), name='api-order-cancel'),
]
