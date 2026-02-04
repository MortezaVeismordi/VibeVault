from django.test import TestCase
from django.contrib.auth.models import User
from apps.shop.models import Category, Product
from .models import Order, OrderItem


class OrderTestCase(TestCase):
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

    def test_order_creation(self):
        order = Order.objects.create(
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
        self.assertEqual(order.order_number, 'ORD001')
        self.assertEqual(order.user, self.user)
