from django.test import TestCase
from .models import Category, Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test Description',
            category=self.category,
            price=99.99,
            sku='TEST001',
            image='products/test.jpg'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 99.99)
