from django.http import JsonResponse
from django.views import View

class PaymentListView(View):
    def get(self, request):
        return JsonResponse({"message": "Payment list API - Coming soon!"})

class ProcessPaymentView(View):
    def post(self, request):
        return JsonResponse({"message": "Process payment API - Coming soon!"}) 