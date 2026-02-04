from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Custom admin for CustomUser model"""
    
    # Display fields in list view
    list_display = (
        'email',
        'get_full_name',
        'is_active',
        'is_verified_email',
        'created_at',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'is_verified_email',
        'is_verified_phone',
        'newsletter_subscribed',
        'created_at',
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    
    # Fieldsets for edit view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "avatar",
                    "bio",
                )
            },
        ),
        (
            _("Address"),
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Verification & Preferences"),
            {
                "fields": (
                    "is_verified_email",
                    "is_verified_phone",
                    "newsletter_subscribed",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login", "created_at", "updated_at", "last_login_ip"),
                "classes": ("collapse",),
            },
        ),
    )
    
    # Fieldsets for add view
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    
    readonly_fields = ("created_at", "updated_at", "last_login_ip")
    
    filter_horizontal = ("groups", "user_permissions")
    
    def get_full_name(self, obj):
        """Display full name in list view"""
        return obj.get_full_name()
    get_full_name.short_description = _("Full Name")
