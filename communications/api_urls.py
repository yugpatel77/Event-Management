from django.urls import path
from . import api_views

app_name = 'communications_api'

urlpatterns = [
    path('conversations/', api_views.ConversationListView.as_view(), name='conversation_list'),
    path('conversations/<int:pk>/messages/', api_views.MessageListView.as_view(), name='message_list'),
] 