from django.urls import path
from . import api_views

app_name = 'venues_api'

urlpatterns = [
    # Venue API endpoints
    path('venues/', api_views.VenueListView.as_view(), name='venue_list'),
    path('venues/<slug:slug>/', api_views.VenueDetailView.as_view(), name='venue_detail'),
    path('venues/search/', api_views.VenueSearchView.as_view(), name='venue_search'),
    
    # 360° Tour API
    path('venues/<slug:slug>/tour/', api_views.Venue360TourView.as_view(), name='venue_tour'),
    path('venues/<slug:slug>/tour/hotspots/', api_views.TourHotspotsView.as_view(), name='tour_hotspots'),
    
    # Venue availability and booking
    path('venues/<slug:slug>/availability/', api_views.VenueAvailabilityView.as_view(), name='venue_availability'),
    path('venues/<slug:slug>/book/', api_views.VenueBookingView.as_view(), name='venue_booking'),
    path('venues/<slug:slug>/packages/', api_views.VenuePackagesView.as_view(), name='venue_packages'),
    
    # Venue reviews
    path('venues/<slug:slug>/reviews/', api_views.VenueReviewsView.as_view(), name='venue_reviews'),
    path('venues/<slug:slug>/reviews/create/', api_views.CreateReviewView.as_view(), name='create_review'),
    
    # Categories
    path('categories/', api_views.VenueCategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/venues/', api_views.CategoryVenuesView.as_view(), name='category_venues'),
] 