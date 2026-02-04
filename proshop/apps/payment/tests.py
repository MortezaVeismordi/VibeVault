from django.test import TestCase
from django.contrib.auth.models import User
from apps.shop.models import Category, Product
from apps.orders.models import Order
from .models import Payment


class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test', slug='test')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test',
            category=self.category,
            price=99.99,
            sku='TEST001',
            image='products/test.jpg'
        )
        self.order = Order.objects.create(
            user=self.user,
            order_number='ORD001',
            shipping_address='123 Main St',
            shipping_city='Test City',
            shipping_state='Test State',
            shipping_postal_code='12345',
            shipping_country='Test Country',
            billing_address='123 Main St',
            billing_city='Test City',
            billing_state='Test State',
            billing_postal_code='12345',
            billing_country='Test Country',
            subtotal=99.99,
            total=99.99
        )

    def test_payment_creation(self):
        payment = Payment.objects.create(
            order=self.order,
            amount=99.99,
            payment_method='card'
        )
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.status, 'pending')
