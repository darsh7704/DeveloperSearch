from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from django.contrib import messages
from users.models import Profile

@login_required
def chat_view(request, username):
    receiver = User.objects.get(username=username)
    receiver_profile = Profile.objects.get(user=receiver)  # Get the profile using user

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Messaage sent succesfully.')

            # Redirect to the receiver's profile using UUID
            return redirect(reverse("user-profile", kwargs={"pk": receiver_profile.id}))

    else:
        form = MessageForm()

    return render(request, "messaging/chat.html", {"form": form, "receiver": receiver_profile.name})

@login_required
def inbox_view(request):
    user_messages = Message.objects.filter(receiver=request.user)
    cnt = Message.objects.filter(receiver=request.user, is_read=False).count()
    return render(request, 'messaging/inbox.html', {'messages_list': user_messages, 'un_read': cnt})

@login_required
def single_view(request, pk):
    message = get_object_or_404(Message, id=pk)

    if not message.is_read:
        message.is_read = True
        message.save() 

    return render(request, 'messaging/single-message.html', {'msgs': message})
