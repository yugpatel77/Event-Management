from django.http import JsonResponse
from django.views import View

class ManagerListView(View):
    def get(self, request):
        return JsonResponse({"message": "Manager list API - Coming soon!"})

class ManagerDetailView(View):
    def get(self, request, slug):
        return JsonResponse({"message": f"Manager detail API for {slug} - Coming soon!"}) 