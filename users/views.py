from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from events.models import Event, Registration
from . import role_required

def home(request):
    """Home page view"""
    return render(request, 'home.html')

def register(request):
    return HttpResponse("Register page - Coming soon!")

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        # Redirect based on user type
        if request.user.user_type == 'user':
            return redirect('users:dashboard')
        elif request.user.user_type == 'manager':
            return redirect('users:manager_dashboard')
        elif request.user.user_type == 'admin':
            return redirect('users:admin_dashboard')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect based on user type
                if user.user_type == 'user':
                    next_url = request.GET.get('next', 'users:dashboard')
                elif user.user_type == 'manager':
                    next_url = request.GET.get('next', 'users:manager_dashboard')
                elif user.user_type == 'admin':
                    next_url = request.GET.get('next', 'users:admin_dashboard')
                else:
                    next_url = request.GET.get('next', 'home')
                
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@role_required(['user'])
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

def edit_profile(request):
    # This view is redundant, profile_view handles edits. Redirecting to profile.
    return redirect('users:profile')

@role_required(['user'])
def change_password(request):
    """Handles password change for logged-in users."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@role_required(['user'])
def dashboard_view(request):
    """User dashboard view"""
    context = {
        'user': request.user,
        'total_events': 0,  # You can add actual counts here
        'total_bookings': 0,
        'recent_activities': [],
    }
    return render(request, 'users/dashboard.html', context)

@role_required(['user'])
def my_events(request):
    """Placeholder view for user's events."""
    context = {
        'page_title': 'My Events',
        'feature_name': 'My Events Page'
    }
    return render(request, 'users/placeholder.html', context)

@role_required(['user'])
def my_bookings(request):
    """Placeholder view for user's bookings."""
    context = {
        'page_title': 'My Bookings',
        'feature_name': 'My Bookings Page'
    }
    return render(request, 'users/placeholder.html', context)

@role_required(['user'])
def my_payments(request):
    """Placeholder view for user's payments."""
    context = {
        'page_title': 'My Payments',
        'feature_name': 'My Payments Page'
    }
    return render(request, 'users/placeholder.html', context)

@role_required(['user'])
def my_messages(request):
    """Placeholder view for user's messages."""
    context = {
        'page_title': 'My Messages',
        'feature_name': 'My Messages Page'
    }
    return render(request, 'users/placeholder.html', context)

@role_required(['admin'])
def admin_dashboard(request):
    events = Event.objects.all()
    registrations = Registration.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'users/admin_dashboard.html', {
        'events': events,
        'registrations': registrations,
        'users': users,
    })

@role_required(['manager'])
def manager_dashboard(request):
    events = Event.objects.filter(event_manager=request.user)
    registrations = Registration.objects.filter(event__event_manager=request.user)
    return render(request, 'users/manager_dashboard.html', {
        'events': events,
        'registrations': registrations,
    })
