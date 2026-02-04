from django.test import TestCase
from django.contrib.auth.models import User
from apps.shop.models import Category, Product
from .models import Cart, CartItem


class CartTestCase(TestCase):
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

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
