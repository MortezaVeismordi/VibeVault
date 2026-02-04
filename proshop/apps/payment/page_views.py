"""
Payment success/cancel pages
"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from apps.orders.models import Order


class OrderSuccessView(View):
    """Display order success page after payment"""
    
    def get(self, request):
        """Show success page"""
        order_id = request.GET.get('order_id')
        session_id = request.GET.get('session_id')
        
        order = None
        if order_id:
            try:
                order = Order.objects.get(id=order_id, user=request.user) if request.user.is_authenticated else Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                pass
        
        context = {
            'order': order,
            'session_id': session_id,
            'message': 'Thank you for your purchase! Your order has been confirmed.'
        }
        return render(request, 'payment/success.html', context)


class OrderCancelView(View):
    """Display order cancel page"""
    
    def get(self, request):
        """Show cancel page"""
        session_id = request.GET.get('session_id')
        
        context = {
            'session_id': session_id,
            'message': 'Your payment was cancelled. No charges have been made to your account.'
        }
        return render(request, 'payment/cancel.html', context)
