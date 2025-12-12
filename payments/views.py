from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def payment_list(request):
    return HttpResponse("Payment list - Coming soon!")

def process_payment(request):
    return HttpResponse("Process payment - Coming soon!")
