"""
Order API Views for REST endpoints
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, filters, pagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderListView(APIView):
    """
    List authenticated user's orders
    GET /api/orders/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get user's orders"""
        try:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            return Response({
                'count': orders.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderDetailView(APIView):
    """
    Get order detail with items
    GET /api/orders/<id>/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        """Get order details"""
        try:
            order = Order.objects.get(id=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderByNumberView(APIView):
    """
    Get order by order number
    GET /api/orders/number/<order_number>/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_number):
        """Get order by number"""
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderCancelView(APIView):
    """
    Cancel an order
    POST /api/orders/<id>/cancel/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Cancel order"""
        try:
            order = Order.objects.get(id=pk, user=request.user)
            
            if order.status in ['pending', 'confirmed']:
                order.status = 'cancelled'
                order.payment_status = 'cancelled'
                order.save()
                return Response({
                    'message': 'Order cancelled successfully',
                    'order_number': order.order_number,
                    'status': order.status
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': f'Cannot cancel order with status {order.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
