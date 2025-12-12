from django.http import JsonResponse
from django.views import View

class EventListView(View):
    def get(self, request):
        return JsonResponse({"message": "Event list API - Coming soon!"})

class EventDetailView(View):
    def get(self, request, pk):
        return JsonResponse({"message": f"Event detail API for {pk} - Coming soon!"}) 