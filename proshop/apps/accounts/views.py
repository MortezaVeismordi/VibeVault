from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from .models import CustomUser


@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request):
    """User registration view"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Validation
        errors = {}
        if not email:
            errors['email'] = 'Email is required.'
        elif CustomUser.objects.filter(email=email).exists():
            errors['email'] = 'This email is already registered.'
        
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        
        if password != password_confirm:
            errors['password_confirm'] = 'Passwords do not match.'
        
        if not first_name or not last_name:
            errors['name'] = 'First and last name are required.'

        if errors:
            return render(request, 'accounts/register.html', {'errors': errors})

        # Create user
        try:
            with transaction.atomic():
                user = CustomUser.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')

    return render(request, 'accounts/register.html')


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('shop')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Update last login IP
            user.last_login_ip = get_client_ip(request)
            user.save(update_fields=['last_login_ip'])
            
            messages.success(request, f'Welcome back, {user.get_display_name()}!')
            next_url = request.GET.get('next', 'shop')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')


@require_http_methods(["POST"])
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('shop')


@login_required(login_url='login')
def profile(request):
    """User profile view"""
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.bio = request.POST.get('bio', user.bio)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        user.country = request.POST.get('country', user.country)
        
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    context = {'user': user}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def change_password(request):
    """Change password view"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()
        
        # Re-authenticate user to keep session
        login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Password changed successfully!')
        return redirect('profile')

    return render(request, 'accounts/change_password.html')


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
