from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from communications.utils import get_allowed_chat_targets
from users import role_required

def dashboard_home(request):
    return HttpResponse("Dashboard home - Coming soon!")

def user_events(request):
    return HttpResponse("User events - Coming soon!")

def user_bookings(request):
    return HttpResponse("User bookings - Coming soon!")

def user_payments(request):
    return HttpResponse("User payments - Coming soon!")

def user_messages(request):
    return HttpResponse("User messages - Coming soon!")

@role_required(['manager'])
def manager_dashboard(request):
    return render(request, 'users/manager_dashboard.html')

def manager_clients(request):
    return HttpResponse("Manager clients - Coming soon!")

def manager_events(request):
    return HttpResponse("Manager events - Coming soon!")

def manager_consultations(request):
    return HttpResponse("Manager consultations - Coming soon!")

def manager_earnings(request):
    return HttpResponse("Manager earnings - Coming soon!")

@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

def admin_users(request):
    return HttpResponse("Admin users - Coming soon!")

def admin_managers(request):
    return HttpResponse("Admin managers - Coming soon!")

def admin_venues(request):
    return HttpResponse("Admin venues - Coming soon!")

def admin_vendors(request):
    return HttpResponse("Admin vendors - Coming soon!")

def admin_events(request):
    return HttpResponse("Admin events - Coming soon!")

def admin_payments(request):
    return HttpResponse("Admin payments - Coming soon!")

def admin_reports(request):
    return HttpResponse("Admin reports - Coming soon!")

@login_required
def dashboard(request):
    allowed_contacts = get_allowed_chat_targets(request.user)
    return render(request, 'users/dashboard.html', {
        'allowed_contacts': allowed_contacts,
    }) 