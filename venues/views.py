from django.shortcuts import render
from users import role_required

# A helper function to render the placeholder page
def _render_placeholder(request, feature_name, page_title):
    context = {'feature_name': feature_name, 'page_title': page_title}
    return render(request, 'users/placeholder.html', context)

# All venue views will now use the placeholder template
def venue_list(request):
    return _render_placeholder(request, "Venue List", "Venues")

@role_required(['user'])
def venue_search(request):
    return _render_placeholder(request, "Venue Search", "Venue Search")

@role_required(['user'])
def venue_list_by_category(request, category_slug):
    return _render_placeholder(request, f"Venues in Category: {category_slug}", "Venues by Category")

@role_required(['user'])
def venue_detail(request, venue_slug):
    return _render_placeholder(request, f"Venue Details for {venue_slug}", "Venue Details")

@role_required(['user'])
def venue_360_tour(request, venue_slug):
    return _render_placeholder(request, f"360° Tour for {venue_slug}", "360° Virtual Tour")

@role_required(['user'])
def venue_gallery(request, venue_slug):
    return _render_placeholder(request, f"Gallery for {venue_slug}", "Venue Gallery")

@role_required(['user'])
def venue_reviews(request, venue_slug):
    return _render_placeholder(request, f"Reviews for {venue_slug}", "Venue Reviews")

@role_required(['user'])
def venue_booking(request, venue_slug):
    return _render_placeholder(request, f"Booking for {venue_slug}", "Book Venue")

@role_required(['user'])
def venue_availability(request, venue_slug):
    return _render_placeholder(request, f"Availability for {venue_slug}", "Venue Availability")

@role_required(['user'])
def venue_packages(request, venue_slug):
    return _render_placeholder(request, f"Packages for {venue_slug}", "Venue Packages")
