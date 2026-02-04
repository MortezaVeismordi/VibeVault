from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem


@login_required(login_url='login')
def order_list(request):
    """Display user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'orders/order_list.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='login')
def create_order(request):
    """Create order from cart"""
    # This is a placeholder - actual implementation would process cart
    context = {}
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'This order cannot be cancelled.')

    return redirect('order_detail', order_id=order.id)
