from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user"""
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom User model for better extensibility and flexibility"""

    # Override default username field with email as unique identifier
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, blank=True)
    
    # Profile fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    
    # Address fields
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Preferences
    is_verified_email = models.BooleanField(default=False, help_text="Email verification status")
    is_verified_phone = models.BooleanField(default=False, help_text="Phone verification status")
    newsletter_subscribed = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Use email as USERNAME_FIELD
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        """Return user's full name"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_display_name(self):
        """Return display name for UI"""
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.email.split("@")[0]

    @property
    def is_complete_profile(self):
        """Check if profile is complete"""
        required_fields = [
            self.first_name,
            self.last_name,
            self.phone,
            self.address,
            self.city,
            self.country,
        ]
        return all(required_fields)
