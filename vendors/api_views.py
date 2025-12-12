from django.http import JsonResponse
from django.views import View

class VendorListView(View):
    def get(self, request):
        return JsonResponse({"message": "Vendor list API - Coming soon!"})

class VendorDetailView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Vendor detail API for {slug} - Coming soon!"}) 