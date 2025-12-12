from django.contrib import admin
from .models import Event, EventType, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'venue', 'start_date', 'organizer', 'status')
    list_filter = ('event_type', 'venue', 'status')
    search_fields = ('title', 'venue__name', 'organizer__username')
    ordering = ('-start_date',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'event_type', 'venue', 'organizer', 'status'),
            'description': 'Fill in the main details of the event.'
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'start_time', 'end_time'),
            'description': 'Set when the event starts and ends.'
        }),
        ('Details', {
            'fields': ('description', 'expected_guests', 'theme'),
            'description': 'Add a description and any special theme.'
        }),
    )

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'event__title')
    list_filter = ('event', 'created_at')
