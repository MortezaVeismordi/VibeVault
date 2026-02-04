"""
Payment processing views with Stripe integration
"""
import stripe
import logging
from decimal import Decimal
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.cart.models import Cart
from apps.orders.models import Order
from apps.payment.models import Payment, PaymentLog

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


class CheckoutView(APIView):
    """
    Create a Stripe checkout session from cart
    POST /api/payment/checkout/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Create Stripe checkout session"""
        try:
            # Get cart
            if request.user.is_authenticated:
                cart = Cart.objects.get_or_create_for_user(request.user)
            else:
                if not request.session.session_key:
                    request.session.create()
                cart = Cart.objects.get_or_create_for_session(request.session.session_key)

            # Validate cart
            if not cart.has_items:
                return Response(
                    {'error': 'Cart is empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check stock
            out_of_stock = []
            for item in cart.items.all():
                if item.quantity > item.variant.stock:
                    out_of_stock.append({
                        'sku': item.variant.sku,
                        'requested': item.quantity,
                        'available': item.variant.stock
                    })

            if out_of_stock:
                return Response(
                    {
                        'error': 'Some items are out of stock',
                        'items': out_of_stock
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Build line items for Stripe
            line_items = []
            for cart_item in cart.items.all():
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"{cart_item.variant.product.name} - {cart_item.variant.name}",
                            'metadata': {
                                'variant_id': str(cart_item.variant.id),
                                'product_id': str(cart_item.variant.product.id),
                            }
                        },
                        'unit_amount': int(cart_item.price_at_add * 100),  # Convert to cents
                    },
                    'quantity': cart_item.quantity,
                })

            # Create Stripe session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=f"{settings.FRONTEND_URL or 'http://localhost:3000'}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL or 'http://localhost:3000'}/checkout/cancel",
                customer_email=request.user.email if request.user.is_authenticated else None,
                metadata={
                    'user_id': str(request.user.id) if request.user.is_authenticated else 'anonymous',
                    'session_key': request.session.session_key if not request.user.is_authenticated else None,
                }
            )

            logger.info(f"Created Stripe checkout session: {session.id}")

            return Response({
                'session_id': session.id,
                'checkout_url': session.url,
                'total_amount': float(cart.total_price),
                'items_count': cart.total_items
            }, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}")
            return Response(
                {'error': 'Failed to create checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WebhookView(APIView):
    """
    Handle Stripe webhook events
    POST /api/payment/webhook/
    """
    permission_classes = [permissions.AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        """Process Stripe webhook"""
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            return HttpResponse(status=400)

        # Return 200 OK immediately to prevent timeout
        response = HttpResponse(status=200)

        # Process event asynchronously (or synchronously for now)
        self._process_event(event)

        return response

    def _process_event(self, event):
        """Process Stripe events"""
        event_type = event['type']
        event_data = event['data']['object']

        logger.info(f"Processing webhook event: {event_type}")

        try:
            if event_type == 'checkout.session.completed':
                self._handle_checkout_completed(event_data)
            elif event_type == 'payment_intent.succeeded':
                self._handle_payment_succeeded(event_data)
            elif event_type == 'charge.failed':
                self._handle_charge_failed(event_data)
            else:
                logger.info(f"Unhandled event type: {event_type}")

        except Exception as e:
            logger.error(f"Error processing event {event_type}: {str(e)}")

    def _handle_checkout_completed(self, session):
        """Handle checkout.session.completed event"""
        session_id = session['id']

        try:
            # Try to find existing order with this session ID
            order = Order.objects.filter(stripe_session_id=session_id).first()

            if not order:
                logger.warning(f"No order found for session {session_id}")
                return

            # Mark order as paid
            order.mark_paid()
            logger.info(f"Order {order.order_number} marked as paid")

            # Reduce stock
            for item in order.items.all():
                if item.variant:
                    item.variant.stock -= item.quantity
                    item.variant.save()
                    logger.info(f"Reduced stock for {item.variant.sku} by {item.quantity}")

            # Create Payment record
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'amount': order.total,
                    'currency': 'USD',
                    'payment_method': 'stripe',
                    'status': 'succeeded',
                    'stripe_session_id': session_id,
                    'stripe_payment_intent_id': session.get('payment_intent'),
                    'completed_at': timezone.now(),
                }
            )

            if not created:
                payment.status = 'succeeded'
                payment.stripe_payment_intent_id = session.get('payment_intent')
                payment.completed_at = timezone.now()
                payment.save()

            # Log event
            PaymentLog.objects.create(
                payment=payment,
                status='succeeded',
                message=f'Payment completed via Stripe session {session_id}',
                response_data=session
            )

            logger.info(f"Payment record created/updated for order {order.order_number}")

        except Order.DoesNotExist:
            logger.error(f"Order not found for session {session_id}")
        except Exception as e:
            logger.error(f"Error handling checkout completed: {str(e)}")

    def _handle_payment_succeeded(self, intent):
        """Handle payment_intent.succeeded event"""
        try:
            payment = Payment.objects.filter(
                stripe_payment_intent_id=intent['id']
            ).first()

            if payment:
                payment.status = 'succeeded'
                payment.completed_at = timezone.now()
                payment.save()

                PaymentLog.objects.create(
                    payment=payment,
                    status='succeeded',
                    message=f'Payment intent {intent["id"]} succeeded',
                    response_data=intent
                )

                logger.info(f"Payment intent {intent['id']} marked as succeeded")

        except Exception as e:
            logger.error(f"Error handling payment succeeded: {str(e)}")

    def _handle_charge_failed(self, charge):
        """Handle charge.failed event"""
        try:
            payment = Payment.objects.filter(
                stripe_charge_id=charge['id']
            ).first()

            if payment:
                payment.status = 'failed'
                payment.save()
                payment.order.mark_failed()

                PaymentLog.objects.create(
                    payment=payment,
                    status='failed',
                    message=f'Charge {charge["id"]} failed: {charge.get("failure_message", "Unknown error")}',
                    response_data=charge
                )

                logger.error(f"Charge {charge['id']} failed for order {payment.order.order_number}")

        except Exception as e:
            logger.error(f"Error handling charge failed: {str(e)}")


class PaymentStatusView(APIView):
    """
    Get payment status for a session
    GET /api/payment/status/?session_id=...
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Get payment status"""
        session_id = request.query_params.get('session_id')

        if not session_id:
            return Response(
                {'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get Stripe session
            session = stripe.checkout.Session.retrieve(session_id)

            # Try to find order
            order = Order.objects.filter(stripe_session_id=session_id).first()

            if order:
                return Response({
                    'session_id': session_id,
                    'stripe_status': session.payment_status,
                    'order_number': order.order_number,
                    'order_status': order.status,
                    'payment_status': order.payment_status,
                    'amount': float(order.total)
                })
            else:
                return Response({
                    'session_id': session_id,
                    'stripe_status': session.payment_status,
                    'message': 'Order not yet created'
                })

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error getting payment status: {str(e)}")
            return Response(
                {'error': 'Failed to get payment status'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

