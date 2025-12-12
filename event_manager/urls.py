"""
URL configuration for event_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('accounts/', include('allauth.urls')),
    # path('', include('two_factor.urls')),
    
    # API endpoints
    path('api/', include('users.api_urls')),
    path('api/', include('venues.api_urls')),
    path('api/', include('events.api_urls')),
    path('api/', include('managers.api_urls')),
    path('api/', include('vendors.api_urls')),
    path('api/', include('payments.api_urls')),
    path('api/', include('communications.api_urls')),
    
    # App URLs
    path('users/', include('users.urls')),
    path('venues/', include('venues.urls')),
    path('events/', include('events.urls')),
    path('managers/', include(('managers.urls', 'managers'), namespace='managers')),
    path('admins/', include(('admins.urls', 'admins'), namespace='admins')),
    path('vendors/', include('vendors.urls')),
    path('payments/', include('payments.urls')),
    path('communications/', include('communications.urls')),
    
    # Main pages (restricted to users only)
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    
    # Additional pages
    path('gallery/', views.gallery_view, name='gallery'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('faq/', views.faq_view, name='faq'),
    
    # Dashboard
    path('dashboard/', include('users.dashboard_urls')),
    
    # Debug toolbar (only in development)
    # path('__debug__/', include('debug_toolbar.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error pages
handler404 = 'event_manager.views.custom_404'
handler500 = 'event_manager.views.custom_500'
