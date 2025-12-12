from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def placeholder_view(request, feature_name, page_title):
    context = {'feature_name': feature_name, 'page_title': page_title}
    return render(request, 'users/placeholder.html', context)

def vendor_list(request):
    return placeholder_view(request, "Vendor List", "Vendors")

def vendor_detail(request, vendor_slug):
    return placeholder_view(request, f"Vendor Details for {vendor_slug}", "Vendor Details")
