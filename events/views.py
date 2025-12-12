from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Event, EventType, Registration
from venues.models import Venue
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from users import role_required

try:
    from .forms import EventForm
except ImportError:
    EventForm = None

# Create your views here.

def event_list(request):
    # Render the custom events page
    return render(request, 'events/event_categories.html')

@role_required(['user'])
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@role_required(['user'])
def event_categories(request):
    return render(request, 'events/event_categories.html')

@role_required(['user'])
def sports_events(request):
    # Get the EventType for Sports
    sports_type = EventType.objects.filter(name__iexact='Sports').first()
    if not sports_type:
        return render(request, 'events/sports_events.html', {'events': [], 'subcategories': [], 'venues': [], 'selected': {}})

    # Get all sports events
    events = Event.objects.filter(event_type=sports_type)

    # Filtering
    subcategory = request.GET.get('subcategory', '')
    date = request.GET.get('date', '')
    location = request.GET.get('location', '')
    skill = request.GET.get('skill', '')
    search = request.GET.get('search', '')

    if subcategory:
        events = events.filter(sub_category__iexact=subcategory)
    if date:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            events = events.filter(start_date=date_obj)
        except ValueError:
            pass
    if location:
        events = events.filter(venue__name__icontains=location)
    if skill:
        events = events.filter(skill_level__iexact=skill)
    if search:
        events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))

    # Subcategories for tabs
    subcategories = events.values_list('sub_category', flat=True).distinct()
    venues = Venue.objects.filter(events__event_type=sports_type).distinct()
    skills = events.values_list('skill_level', flat=True).distinct()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(events, 6)  # 6 events per page
    try:
        events_page = paginator.page(page)
    except PageNotAnInteger:
        events_page = paginator.page(1)
    except EmptyPage:
        events_page = paginator.page(paginator.num_pages)

    context = {
        'events': events_page,
        'subcategories': subcategories,
        'venues': venues,
        'skills': skills,
        'selected': {
            'subcategory': subcategory,
            'date': date,
            'location': location,
            'skill': skill,
            'search': search,
        },
        'page_obj': events_page,
        'paginator': paginator,
    }
    return render(request, 'events/sports_events.html', context)

@role_required(['user'])
def adventure_events(request):
    return render(request, 'events/adventure_events.html')

@role_required(['user'])
def music_events(request):
    return render(request, 'events/music_events.html')

@role_required(['user'])
def cooking_events(request):
    return render(request, 'events/cooking_events.html')

@role_required(['user'])
def coding_events(request):
    return render(request, 'events/coding_events.html')

@role_required(['user'])
def movie_events(request):
    return render(request, 'events/movie_events.html')

@role_required(['user'])
def event_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    city = event.venue.city.lower() if hasattr(event.venue, 'city') else ''
    if city not in ['ahmedabad', 'gandhinagar']:
        messages.error(request, 'Registration is only allowed for events in Ahmedabad or Gandhinagar.')
        return redirect('events:event_detail', event_id=event.id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if name and email and phone:
            reg = Registration.objects.create(event=event, name=name, email=email, phone=phone)
            # Send email to user
            send_mail(
                subject=f'Registration Confirmation for {event.title}',
                message=f'Thank you {name} for registering for {event.title}!',
                from_email=None,
                recipient_list=[email],
                fail_silently=True,
            )
            # Send email to event manager
            if event.event_manager and event.event_manager.email:
                send_mail(
                    subject=f'New Registration for {event.title}',
                    message=f'{name} ({email}, {phone}) registered for your event.',
                    from_email=None,
                    recipient_list=[event.event_manager.email],
                    fail_silently=True,
                )
            messages.success(request, 'Registration successful! A confirmation email has been sent.')
            return redirect('events:booking_page')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'events/event_registration.html', {'event': event})

@role_required(['user'])
def booking_page(request):
    # Show all registrations for the current user (by email if logged in, else show none)
    user_email = request.user.email if request.user.is_authenticated else None
    bookings = Registration.objects.filter(email=user_email) if user_email else []
    return render(request, 'events/booking_page.html', {'bookings': bookings})

def is_manager(user):
    return user.groups.filter(name='Event Managers').exists() or user.is_superuser

@role_required(['manager'])
def add_event(request):
    # Remove EventForm and add_event view for now
    pass
