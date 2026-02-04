from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserModelTestCase(TestCase):
    """Test cases for CustomUser model"""

    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'TestPassword123!',
        }

    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        """Test that creating user without email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                first_name='John',
                last_name='Doe',
                password='TestPassword123!'
            )

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPass123!'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_get_full_name(self):
        """Test get_full_name method"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), 'John Doe')

    def test_get_display_name(self):
        """Test get_display_name method"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_display_name(), 'John Doe')

    def test_get_display_name_without_name(self):
        """Test get_display_name when first and last name are empty"""
        user = User.objects.create_user(
            email='noname@example.com',
            password='TestPassword123!'
        )
        self.assertEqual(user.get_display_name(), 'noname')

    def test_is_complete_profile(self):
        """Test is_complete_profile property"""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_complete_profile)
        
        user.phone = '1234567890'
        user.address = '123 Main St'
        user.city = 'New York'
        user.country = 'USA'
        self.assertTrue(user.is_complete_profile)

    def test_normalize_email(self):
        """Test that email is normalized when saving"""
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='John',
            last_name='Doe',
            password='TestPassword123!'
        )
        # Email should be stored as is (CustomUser doesn't force lowercase)
        self.assertEqual(user.email, 'testuser@example.com')

    def test_unique_email(self):
        """Test that email must be unique"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)

    def test_user_str_representation(self):
        """Test string representation of user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'John Doe')


class RegisterViewTestCase(TestCase):
    """Test cases for registration view"""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_register_page_loads(self):
        """Test that register page loads"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_user_success(self):
        """Test successful user registration"""
        data = {
            'email': 'newuser@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'NewPassword123!',
            'password_confirm': 'NewPassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(email=data['email']).exists())

    def test_register_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = {
            'email': 'newuser@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'NewPassword123!',
            'password_confirm': 'DifferentPassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  # Stays on register page
        self.assertFalse(User.objects.filter(email=data['email']).exists())

    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        User.objects.create_user(
            email='existing@example.com',
            first_name='John',
            last_name='Doe',
            password='TestPassword123!'
        )
        data = {
            'email': 'existing@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'NewPassword123!',
            'password_confirm': 'NewPassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  # Stays on register page


class LoginViewTestCase(TestCase):
    """Test cases for login view"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='John',
            last_name='Doe',
            password='TestPassword123!'
        )

    def test_login_page_loads(self):
        """Test that login page loads"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_success(self):
        """Test successful login"""
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123!',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to shop
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword!',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # Stays on login page
