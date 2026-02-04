"""
Management command to populate database with sample data for testing
Usage: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.shop.models import Category, Product
from apps.orders.models import Order, OrderItem
from decimal import Decimal
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new sample data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Category.objects.all().delete()
            Product.objects.all().delete()
            Order.objects.filter(user__username__startswith='customer').delete()
            User.objects.filter(username__startswith='customer').delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared!'))

        # Create sample users
        self.stdout.write('Creating sample users...')
        users = []
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f'customer{i}',
                defaults={
                    'email': f'customer{i}@example.com',
                    'first_name': f'Customer',
                    'last_name': f'User{i}'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created user: {user.username}'))
            else:
                self.stdout.write(f'  → User already exists: {user.username}')
            users.append(user)

        # Create sample categories
        self.stdout.write('Creating sample categories...')
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Home & Kitchen', 'description': 'Home and kitchen essentials'},
            {'name': 'Sports', 'description': 'Sports and outdoor equipment'},
            {'name': 'Books', 'description': 'Books and reading materials'},
        ]
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {cat.name}'))
            else:
                self.stdout.write(f'  → Category already exists: {cat.name}')
            categories.append(cat)

        # Create sample products
        self.stdout.write('Creating sample products...')
        products_data = [
            {
                'name': 'Wireless Bluetooth Headphones',
                'category': categories[0],
                'price': Decimal('79.99'),
                'description': 'Premium wireless headphones with noise cancellation'
            },
            {
                'name': '4K Webcam',
                'category': categories[0],
                'price': Decimal('149.99'),
                'description': 'Ultra HD webcam for streaming and video calls'
            },
            {
                'name': 'USB-C Cable Pack',
                'category': categories[0],
                'price': Decimal('24.99'),
                'description': '5-pack of durable USB-C charging cables'
            },
            {
                'name': 'Cotton T-Shirt',
                'category': categories[1],
                'price': Decimal('29.99'),
                'description': '100% organic cotton comfortable t-shirt'
            },
            {
                'name': 'Denim Jeans',
                'category': categories[1],
                'price': Decimal('59.99'),
                'description': 'Classic denim jeans with modern fit'
            },
            {
                'name': 'Non-Stick Cookware Set',
                'category': categories[2],
                'price': Decimal('89.99'),
                'description': '10-piece non-stick cookware set'
            },
            {
                'name': 'Stainless Steel Kettle',
                'category': categories[2],
                'price': Decimal('34.99'),
                'description': 'Modern stainless steel electric kettle'
            },
            {
                'name': 'Yoga Mat',
                'category': categories[3],
                'price': Decimal('49.99'),
                'description': 'Non-slip yoga mat with carrying strap'
            },
            {
                'name': 'Dumbbell Set',
                'category': categories[3],
                'price': Decimal('129.99'),
                'description': 'Adjustable 5-25 lb dumbbell set'
            },
            {
                'name': 'Python Programming Book',
                'category': categories[4],
                'price': Decimal('44.99'),
                'description': 'Comprehensive guide to Python programming'
            },
        ]

        products = []
        for prod_data in products_data:
            prod, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': prod_data['category'],
                    'price': prod_data['price'],
                    'description': prod_data['description'],
                    'stock': random.randint(5, 50)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created product: {prod.name}'))
            else:
                self.stdout.write(f'  → Product already exists: {prod.name}')
            products.append(prod)

        # Create sample orders
        self.stdout.write('Creating sample orders...')
        for i, user in enumerate(users):
            order, created = Order.objects.get_or_create(
                order_number=f'ORD{datetime.now().strftime("%Y%m%d")}{1000+i}',
                user=user,
                defaults={
                    'total_amount': Decimal('0.00'),
                    'status': random.choice(['pending', 'processing', 'completed', 'cancelled']),
                    'payment_status': random.choice(['pending', 'completed']),
                    'created_at': datetime.now() - timedelta(days=random.randint(1, 30)),
                }
            )
            
            if created:
                # Add random items to order
                selected_products = random.sample(products, random.randint(2, 5))
                total = Decimal('0.00')
                
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    price = product.price
                    subtotal = price * quantity
                    
                    OrderItem.objects.get_or_create(
                        order=order,
                        product=product,
                        defaults={
                            'quantity': quantity,
                            'price': price,
                            'subtotal': subtotal
                        }
                    )
                    total += subtotal
                
                order.total_amount = total
                order.save()
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Created order {order.order_number} for {user.username} (${total})'
                ))
            else:
                self.stdout.write(f'  → Order already exists: {order.order_number}')

        self.stdout.write(self.style.SUCCESS('\n✓ Sample data created successfully!'))
        self.stdout.write(self.style.WARNING(
            '\nTest Account Details:\n'
            '  Username: customer1\n'
            '  Email: customer1@example.com\n'
            '  Password: password123\n'
        ))
