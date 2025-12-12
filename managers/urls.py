from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.manager_list, name='manager_list'),
    path('<slug:manager_slug>/', views.manager_detail, name='manager_detail'),
] 