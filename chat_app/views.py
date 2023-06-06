# chat/views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from accounts.types import UserState

User = get_user_model()


def index(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    context = {}
    return render(request, "index.html", context)

def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})

def connect(request):
    room_name = ""
    user = request.user
    online_users = User.objects.filter(
        status=UserState.ONLINE,
    ).exclude(user_id=user.user_id)
    
    if not online_users.count():
        messages.error(request, 'No one is online!', 'danger')
        return redirect("accounts:add_interest")

    users_with_similar_interest = online_users.filter(interests__in=user.interests.all())

    if users_with_similar_interest.count():
        first_user_interests = user.interests.all()
        second_user_interests = users_with_similar_interest.first().interests.all()

        room_name = first_user_interests.intersection(second_user_interests).first().name
    else:
        final_user = online_users.first()
        room_name = final_user.interests.first().name
    
    return redirect("chat_app:chat_room", room_name=room_name)