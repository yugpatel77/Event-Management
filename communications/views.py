from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from users.models import CustomUser
from communications.models import Conversation, Message
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from django.urls import reverse
from .forms import GroupChatCreateForm
from .models import ChatRoom, ChatRoomMember, ChatMessage, GroupJoinRequest
from django.utils import timezone
from users import role_required

# Create your views here.

@role_required(['user'])
def conversation_list(request):
    return HttpResponse("Conversation list - Coming soon!")

@role_required(['user'])
def chat_room(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.order_by('created_at')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
            return redirect('communications:chat_room', conversation_id=conversation.id)
    return render(request, 'communications/chat_room.html', {
        'conversation': conversation,
        'messages': messages,
    })

@role_required(['user'])
def start_chat(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    # Ensure consistent ordering for unique_together
    user1, user2 = (request.user, target_user) if request.user.id < target_user.id else (target_user, request.user)
    # Determine conversation_type
    if user1.user_type == 'user' and user2.user_type == 'manager':
        conversation_type = 'user_manager'
    elif user1.user_type == 'manager' and user2.user_type == 'user':
        conversation_type = 'user_manager'
    elif user1.user_type == 'admin' or user2.user_type == 'admin':
        conversation_type = 'admin_user' if 'user' in [user1.user_type, user2.user_type] else 'admin_manager'
    else:
        conversation_type = 'user_manager'
    conversation = Conversation.objects.filter(participant1=user1, participant2=user2).first()
    if not conversation:
        conversation = Conversation.objects.create(participant1=user1, participant2=user2, conversation_type=conversation_type)
    return redirect('communications:chat_room', conversation_id=conversation.id)

@role_required(['user'])
def conversation_inbox(request):
    # 1-to-1 conversations
    conversations = Conversation.objects.filter(
        models.Q(participant1=request.user) | models.Q(participant2=request.user)
    ).order_by('-last_message_at', '-created_at')
    for conv in conversations:
        conv.unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
    # Group chats
    group_memberships = ChatRoomMember.objects.filter(user=request.user, is_active=True).select_related('room')
    group_chats = []
    for membership in group_memberships:
        room = membership.room
        room.last_message = room.messages.order_by('-created_at').first()
        if membership.last_read_at:
            room.unread_count = room.messages.filter(created_at__gt=membership.last_read_at, is_edited=False, is_deleted=False).exclude(sender=request.user).count()
        else:
            room.unread_count = room.messages.filter(is_edited=False, is_deleted=False).exclude(sender=request.user).count()
        group_chats.append(room)
    return render(request, 'communications/inbox.html', {
        'conversations': conversations,
        'group_chats': group_chats,
        'user': request.user,
    })

@role_required(['manager', 'admin'])
def create_group(request):
    if not (request.user.user_type in ['manager', 'admin'] or request.user.is_superuser):
        messages.error(request, 'You do not have permission to create a group.')
        return redirect(reverse('communications:inbox'))
    if request.method == 'POST':
        form = GroupChatCreateForm(request.POST, current_user=request.user)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.is_private = True
            chat_room.save()
            # Add creator as admin
            ChatRoomMember.objects.create(room=chat_room, user=request.user, role='admin')
            # Add selected users as members
            for user in form.cleaned_data['users']:
                ChatRoomMember.objects.create(room=chat_room, user=user, role='member')
            messages.success(request, 'Group chat created successfully!')
            return redirect('communications:group_chat_room', room_id=chat_room.id)
    else:
        form = GroupChatCreateForm(current_user=request.user)
    return render(request, 'communications/create_group.html', {'form': form})

@role_required(['user'])
def group_chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    # Only allow members
    member = ChatRoomMember.objects.filter(room=room, user=request.user, is_active=True).first()
    if not member:
        messages.error(request, 'You are not a member of this group.')
        return redirect('communications:inbox')
    # Update last_read_at to now
    member.last_read_at = timezone.now()
    member.save(update_fields=["last_read_at"])
    messages_qs = room.messages.order_by('created_at')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ChatMessage.objects.create(room=room, sender=request.user, content=content)
            return redirect('communications:group_chat_room', room_id=room.id)
    return render(request, 'communications/group_chat_room.html', {
        'room': room,
        'messages': messages_qs,
        'member_role': member.role,
    })

@role_required(['manager', 'admin'])
def add_users_to_group(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    # Exclude users already in the group
    current_member_ids = room.members.values_list('user_id', flat=True)
    available_users = CustomUser.objects.exclude(id__in=current_member_ids)
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        for user_id in user_ids:
            user = CustomUser.objects.get(id=user_id)
            # Determine role hierarchy
            hierarchy = {'user': 1, 'manager': 2, 'admin': 3, 'superadmin': 4}
            req_rank = hierarchy.get(getattr(request.user, 'user_type', 'user'), 1)
            target_rank = hierarchy.get(getattr(user, 'user_type', 'user'), 1)
            # Superadmin can only be added by request
            if getattr(user, 'is_superuser', False) or target_rank > req_rank:
                # Create join request if not already pending
                if not GroupJoinRequest.objects.filter(room=room, target_user=user, status='pending').exists():
                    GroupJoinRequest.objects.create(room=room, requested_by=request.user, target_user=user)
            else:
                ChatRoomMember.objects.get_or_create(room=room, user=user, defaults={'role': 'member'})
        messages.success(request, 'Users added or requests sent!')
        return redirect('communications:group_chat_room', room_id=room.id)
    return render(request, 'communications/add_users_to_group.html', {
        'room': room,
        'available_users': available_users,
    })

@role_required(['user'])
def group_join_requests(request):
    # Show join requests for the current user (superadmin or higher-rank)
    requests = GroupJoinRequest.objects.filter(target_user=request.user, status='pending')
    return render(request, 'communications/group_join_requests.html', {'requests': requests})

@role_required(['user'])
def handle_join_request(request, request_id, action):
    join_request = get_object_or_404(GroupJoinRequest, id=request_id, target_user=request.user)
    if join_request.status != 'pending':
        messages.info(request, 'This request has already been handled.')
        return redirect('communications:group_join_requests')
    if action == 'accept':
        ChatRoomMember.objects.get_or_create(room=join_request.room, user=request.user, defaults={'role': 'member'})
        join_request.status = 'accepted'
    else:
        join_request.status = 'declined'
    from django.utils import timezone
    join_request.responded_at = timezone.now()
    join_request.save()
    messages.success(request, f'Request {action}ed.')
    return redirect('communications:group_join_requests')
