from django.db import models
from django.conf import settings
from apps.shop.models import Product


class Review(models.Model):
    """Product reviews and ratings"""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    helpful_count = models.IntegerField(default=0)
    verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ReviewImage(models.Model):
    """Images attached to reviews"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for review by {self.review.user.username}"


class ReviewVote(models.Model):
    """Track helpful votes on reviews"""
    VOTE_CHOICES = [
        ('helpful', 'Helpful'),
        ('unhelpful', 'Unhelpful'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_votes')
    vote_type = models.CharField(max_length=20, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on review by {self.review.user.username}"
