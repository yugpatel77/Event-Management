from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['event_manager', 'organizer']
        fields = [
            'title', 'description', 'event_type', 'sub_category', 'start_date', 'end_date', 'start_time', 'end_time',
            'expected_guests', 'venue', 'venue_package', 'status', 'total_budget', 'venue_cost', 'vendor_costs',
            'manager_fee', 'total_cost', 'theme', 'color_scheme', 'special_requirements', 'dietary_restrictions',
            'setup_time', 'cleanup_time', 'setup_requirements', 'event_image', 'skill_level', 'format', 'tags'
        ] 