from django.http import JsonResponse
from django.views import View

class VenueListView(View):
    def get(self, request):
        return JsonResponse({"message": "Venue list API - Coming soon!"})

class VenueDetailView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Venue detail API for {slug} - Coming soon!"})

class VenueSearchView(View):
    def get(self, request):
        return JsonResponse({"message": "Venue search API - Coming soon!"})

class Venue360TourView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"360° tour API for {slug} - Coming soon!"})

class TourHotspotsView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Tour hotspots API for {slug} - Coming soon!"})

class VenueAvailabilityView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Availability API for {slug} - Coming soon!"})

class VenueBookingView(View):
    def post(self, request, slug):
        return JsonResponse({"message": f"Booking API for {slug} - Coming soon!"})

class VenuePackagesView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Packages API for {slug} - Coming soon!"})

class VenueReviewsView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Reviews API for {slug} - Coming soon!"})

class CreateReviewView(View):
    def post(self, request, slug):
        return JsonResponse({"message": f"Create review API for {slug} - Coming soon!"})

class VenueCategoryListView(View):
    def get(self, request):
        return JsonResponse({"message": "Category list API - Coming soon!"})

class CategoryVenuesView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Category venues API for {slug} - Coming soon!"}) 