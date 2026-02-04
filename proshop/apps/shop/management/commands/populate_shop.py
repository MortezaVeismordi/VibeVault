"""
Management command to populate shop with sample data
Usage: python manage.py populate_shop
"""
import json
from django.core.management.base import BaseCommand
from apps.shop.models import Category, Product, ProductVariant


class Command(BaseCommand):
    help = 'Populate database with sample shop data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[INFO] Starting sample data creation...'))

        # Create categories
        electronics = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic devices and gadgets',
            icon='📱',
            is_active=True,
            ordering=1
        )

        smartphones = Category.objects.create(
            name='Smartphones',
            slug='smartphones',
            description='Mobile phones and smartphones',
            icon='📞',
            parent=electronics,
            is_active=True,
            ordering=1
        )

        laptops = Category.objects.create(
            name='Laptops',
            slug='laptops',
            description='Laptop computers and notebooks',
            icon='💻',
            parent=electronics,
            is_active=True,
            ordering=2
        )

        accessories = Category.objects.create(
            name='Accessories',
            slug='accessories',
            description='Phone and device accessories',
            icon='🎧',
            parent=electronics,
            is_active=True,
            ordering=3
        )

        clothing = Category.objects.create(
            name='Clothing',
            slug='clothing',
            description='Fashion and apparel',
            icon='👕',
            is_active=True,
            ordering=2
        )

        self.stdout.write('  * Categories created successfully')

        # Create products with variants
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'sku': 'IPHONE-15-PRO',
                'brand': 'Apple',
                'category': smartphones,
                'description': 'Latest Apple smartphone with advanced features',
                'short_description': 'Premium smartphone',
                'base_price': '999.99',
                'cost_price': '650.00',
                'is_featured': True,
                'is_new': True,
                'meta_title': 'iPhone 15 Pro - Premium Smartphone',
                'meta_description': 'Latest iPhone 15 Pro with advanced camera and processing',
                'variants': [
                    {'sku': 'IPHONE-15-PRO-BLK-128', 'price': '999.99', 'cost_price': '650.00', 'stock': 50, 'attributes': {'color': 'Black', 'storage': '128GB'}, 'is_default': True},
                    {'sku': 'IPHONE-15-PRO-WHT-256', 'price': '1099.99', 'cost_price': '700.00', 'stock': 30, 'attributes': {'color': 'White', 'storage': '256GB'}},
                    {'sku': 'IPHONE-15-PRO-GLD-512', 'price': '1199.99', 'cost_price': '750.00', 'stock': 20, 'attributes': {'color': 'Gold', 'storage': '512GB'}},
                ]
            },
            {
                'name': 'Samsung Galaxy S24',
                'sku': 'SAMSUNG-S24',
                'brand': 'Samsung',
                'category': smartphones,
                'description': 'Flagship Samsung smartphone with AI features',
                'short_description': 'AI-powered smartphone',
                'base_price': '899.99',
                'cost_price': '550.00',
                'is_featured': True,
                'meta_title': 'Samsung Galaxy S24',
                'meta_description': 'Flagship smartphone with advanced AI capabilities',
                'variants': [
                    {'sku': 'SAMSUNG-S24-BLK-256', 'price': '899.99', 'cost_price': '550.00', 'stock': 40, 'attributes': {'color': 'Black', 'storage': '256GB'}, 'is_default': True},
                    {'sku': 'SAMSUNG-S24-SLV-512', 'price': '999.99', 'cost_price': '600.00', 'stock': 25, 'attributes': {'color': 'Silver', 'storage': '512GB'}},
                ]
            },
            {
                'name': 'MacBook Pro 16"',
                'sku': 'MACBOOK-PRO-16',
                'brand': 'Apple',
                'category': laptops,
                'description': 'Powerful laptop for professionals and developers',
                'short_description': 'Professional laptop',
                'base_price': '2499.99',
                'cost_price': '1500.00',
                'is_featured': True,
                'is_bestseller': True,
                'meta_title': 'MacBook Pro 16 inch',
                'meta_description': 'Professional laptop with M4 chip and retina display',
                'variants': [
                    {'sku': 'MACBOOK-PRO-M4-16GB', 'price': '2499.99', 'cost_price': '1500.00', 'stock': 15, 'attributes': {'chip': 'M4', 'ram': '16GB', 'storage': '512GB'}, 'is_default': True},
                    {'sku': 'MACBOOK-PRO-M4-32GB', 'price': '2999.99', 'cost_price': '1800.00', 'stock': 10, 'attributes': {'chip': 'M4', 'ram': '32GB', 'storage': '1TB'}},
                ]
            },
            {
                'name': 'Dell XPS 13',
                'sku': 'DELL-XPS-13',
                'brand': 'Dell',
                'category': laptops,
                'description': 'Ultraportable laptop with stunning display',
                'short_description': 'Compact and powerful',
                'base_price': '1299.99',
                'cost_price': '750.00',
                'is_featured': True,
                'meta_title': 'Dell XPS 13 Laptop',
                'meta_description': 'Ultraportable Dell XPS 13 with FHD display',
                'variants': [
                    {'sku': 'DELL-XPS-13-I7', 'price': '1299.99', 'cost_price': '750.00', 'stock': 20, 'attributes': {'processor': 'Intel i7', 'ram': '16GB'}, 'is_default': True},
                    {'sku': 'DELL-XPS-13-I9', 'price': '1599.99', 'cost_price': '900.00', 'stock': 12, 'attributes': {'processor': 'Intel i9', 'ram': '32GB'}},
                ]
            },
            {
                'name': 'AirPods Pro',
                'sku': 'AIRPODS-PRO',
                'brand': 'Apple',
                'category': accessories,
                'description': 'Premium wireless earbuds with noise cancellation',
                'short_description': 'Wireless earbuds',
                'base_price': '249.99',
                'cost_price': '120.00',
                'is_featured': True,
                'is_bestseller': True,
                'meta_title': 'AirPods Pro',
                'meta_description': 'Premium wireless earbuds with active noise cancellation',
                'variants': [
                    {'sku': 'AIRPODS-PRO-GEN2', 'price': '249.99', 'cost_price': '120.00', 'stock': 100, 'attributes': {'generation': '2nd Gen', 'color': 'White'}, 'is_default': True},
                ]
            },
            {
                'name': 'Premium T-Shirt',
                'sku': 'TSHIRT-PREMIUM',
                'brand': 'StyleCo',
                'category': clothing,
                'description': 'High-quality cotton t-shirt',
                'short_description': 'Comfortable t-shirt',
                'base_price': '29.99',
                'cost_price': '10.00',
                'is_featured': False,
                'meta_title': 'Premium Cotton T-Shirt',
                'meta_description': 'Comfortable and durable cotton t-shirt',
                'variants': [
                    {'sku': 'TSHIRT-S-BLACK', 'price': '29.99', 'cost_price': '10.00', 'stock': 200, 'attributes': {'size': 'S', 'color': 'Black'}, 'is_default': True},
                    {'sku': 'TSHIRT-M-BLACK', 'price': '29.99', 'cost_price': '10.00', 'stock': 250, 'attributes': {'size': 'M', 'color': 'Black'}},
                    {'sku': 'TSHIRT-L-BLACK', 'price': '29.99', 'cost_price': '10.00', 'stock': 180, 'attributes': {'size': 'L', 'color': 'Black'}},
                    {'sku': 'TSHIRT-XL-BLACK', 'price': '29.99', 'cost_price': '10.00', 'stock': 150, 'attributes': {'size': 'XL', 'color': 'Black'}},
                    {'sku': 'TSHIRT-S-WHITE', 'price': '29.99', 'cost_price': '10.00', 'stock': 180, 'attributes': {'size': 'S', 'color': 'White'}},
                    {'sku': 'TSHIRT-M-WHITE', 'price': '29.99', 'cost_price': '10.00', 'stock': 200, 'attributes': {'size': 'M', 'color': 'White'}},
                ]
            },
        ]

        created_count = 0
        for product_data in products_data:
            variants = product_data.pop('variants', [])
            
            product = Product.objects.create(
                **product_data
            )

            for variant_data in variants:
                ProductVariant.objects.create(
                    product=product,
                    **variant_data
                )

            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} products with variants'))
        self.stdout.write(self.style.SUCCESS('[DONE] Sample data creation completed!\n'))
        self.stdout.write(self.style.WARNING(f'Summary:'))
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Products: {Product.objects.count()}')
        self.stdout.write(f'  Variants: {ProductVariant.objects.count()}')
