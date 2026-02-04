"""Custom mixins for views"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin access"""
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')


class OwnerRequiredMixin(UserPassesTestMixin):
    """Mixin to require owner access"""
    def test_func(self):
        return self.request.user == self.get_object().user

    def handle_no_permission(self):
        return redirect('home')
