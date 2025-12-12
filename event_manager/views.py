from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from users import role_required

def home_view(request):
    """Home page - accessible to everyone"""
    return render(request, 'event_manager/home.html')

def about_view(request):
    """About page - accessible to everyone"""
    return render(request, 'about.html')

def contact_view(request):
    """Contact page - accessible to everyone"""
    return render(request, 'contact.html')

def privacy_view(request):
    """Privacy page - accessible to everyone"""
    return render(request, 'privacy.html')

def terms_view(request):
    """Terms page - accessible to everyone"""
    return render(request, 'terms.html')

def gallery_view(request):
    """Event gallery page - accessible to everyone"""
    return render(request, 'events/event_gallery.html')

def testimonials_view(request):
    """Testimonials page - accessible to everyone"""
    return render(request, 'testimonials.html')

def pricing_view(request):
    """Pricing page - accessible to everyone"""
    return render(request, 'pricing.html')

def faq_view(request):
    """FAQ page - accessible to everyone"""
    return render(request, 'faq.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500) 