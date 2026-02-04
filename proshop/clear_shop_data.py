#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proshop.settings')
django.setup()

from apps.shop.models import Category, Product

# Clear existing data
deleted_count, _ = Category.objects.all().delete()
print(f"Deleted {deleted_count} categories and related objects")
