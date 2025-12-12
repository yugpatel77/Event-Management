from django.http import JsonResponse
from django.views import View

class UserRegistrationView(View):
    def post(self, request):
        return JsonResponse({"message": "Registration API - Coming soon!"})

class UserLoginView(View):
    def post(self, request):
        return JsonResponse({"message": "Login API - Coming soon!"})

class UserLogoutView(View):
    def post(self, request):
        return JsonResponse({"message": "Logout API - Coming soon!"})

class UserProfileView(View):
    def get(self, request):
        return JsonResponse({"message": "Profile API - Coming soon!"})

class UserListView(View):
    def get(self, request):
        return JsonResponse({"message": "User list API - Coming soon!"})

class UserDetailView(View):
    def get(self, request, pk):
        return JsonResponse({"message": f"User detail API for {pk} - Coming soon!"})

class ProfileUpdateView(View):
    def post(self, request):
        return JsonResponse({"message": "Profile update API - Coming soon!"}) 