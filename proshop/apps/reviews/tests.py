from django.test import TestCase
from django.contrib.auth.models import User
from apps.shop.models import Category, Product
from .models import Review


class ReviewTestCase(TestCase):
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

    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            title='Great Product',
            content='This is a great product!',
            rating=5
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user, self.user)
