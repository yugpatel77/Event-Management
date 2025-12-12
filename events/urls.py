from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('categories/', views.event_categories, name='event_categories'),
    path('sports/', views.sports_events, name='sports_events'),
    path('adventure/', views.adventure_events, name='adventure_events'),
    path('music/', views.music_events, name='music_events'),
    path('cooking/', views.cooking_events, name='cooking_events'),
    path('coding/', views.coding_events, name='coding_events'),
    path('movies/', views.movie_events, name='movie_events'),
    path('<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('bookings/', views.booking_page, name='booking_page'),
    path('add/', views.add_event, name='add_event'),
] 