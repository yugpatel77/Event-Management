from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import ManagerCreationForm, ManagerAuthenticationForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from users import role_required

# Create your views here.

def manager_list(request):
    return HttpResponse("Manager list - Coming soon!")

def manager_detail(request, manager_slug):
    return HttpResponse(f"Manager detail for {manager_slug} - Coming soon!")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:manager_dashboard')
    if request.method == 'POST':
        form = ManagerAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.user_type == 'manager':
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('users:manager_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a manager account.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ManagerAuthenticationForm()
    return render(request, 'managers/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('managers:dashboard')
    if request.method == 'POST':
        form = ManagerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('managers:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ManagerCreationForm()
    return render(request, 'managers/register.html', {'form': form})

@role_required(['manager'])
def dashboard_view(request):
    return render(request, 'managers/dashboard.html', {'user': request.user})
