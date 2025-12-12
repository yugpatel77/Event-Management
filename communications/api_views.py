from django.http import JsonResponse
from django.views import View

class ConversationListView(View):
    def get(self, request):
        return JsonResponse({"message": "Conversation list API - Coming soon!"})

class MessageListView(View):
    def get(self, request, pk):
        return JsonResponse({"message": f"Message list API for conversation {pk} - Coming soon!"}) 