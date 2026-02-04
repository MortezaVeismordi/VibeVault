from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model with timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    """Manager for active/inactive model"""
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)
