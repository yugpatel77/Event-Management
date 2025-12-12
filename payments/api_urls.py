from django.urls import path
from . import api_views

app_name = 'payments_api'

urlpatterns = [
    path('payments/', api_views.PaymentListView.as_view(), name='payment_list'),
    path('payments/process/', api_views.ProcessPaymentView.as_view(), name='process_payment'),
] 