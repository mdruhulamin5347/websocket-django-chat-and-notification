from django.shortcuts import render,redirect
from .forms import UserAuthForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Notification,Chat

from django.contrib.auth.models import User
# Create your views here.


def Registration(request):
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserAuthForm()
    return render(request,'registration.html',{'form':form})

def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request , data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})

 
# def Home(request):
#     return render(request, 'home.html')

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def create_notification(request):
    notifications= Notification.objects.filter(user=request.user)
    return render(request, 'home.html',{'notifications':notifications})



def UserList(request):
    users = User.objects.exclude(pk=request.user.pk)  # Fetch all users except the current one
    user_chat_list = []
    
    for user in users:
        last_message_sent = Chat.objects.filter(sender=user, receiver=request.user).last()
        last_message_receive = Chat.objects.filter(receiver=user, sender=request.user).last()  # Fetch the latest message sent by the user
        if last_message_sent and (not last_message_receive or last_message_sent.created_at > last_message_receive.created_at):
             latest_message = last_message_sent 
        else:
            latest_message = last_message_receive
        
        user_chat_list.append({
            'user': user,
            'last_message': latest_message
        })

    return render(request, 'userlist.html', {'user_chat_list': user_chat_list})


def ChatView(request,id):
    receive = get_object_or_404(User, id=id)
    print(receive.id)
    send = request.user
    sender_message = Chat.objects.filter(sender=send, receiver=receive)
    receiver_message = Chat.objects.filter(sender=receive, receiver=send)
    all_message = sender_message | receiver_message
    all_message = all_message.order_by('created_at')
    if request.method== 'POST':
        message = request.POST.get('message')
        if message:
            chat, created = Chat.objects.get_or_create(sender=send, receiver=receive, message=message)

            notify, created = Notification.objects.get_or_create(user=receive, message = message)
            notify.save()
            channel_layer = get_channel_layer()

            # Send notification to 'notifications' group
            async_to_sync(channel_layer.group_send)(
                'notifications',  # The group name
                {
                    'type': 'send_notification',
                    'message': message,
                    'username': request.user.username, 
                }
            )

            # Send chat message to the group for WebSocket handling
            async_to_sync(channel_layer.group_send)(
                'chat_room_group',  # Group for chat
                {
                    'type': 'send_chat_message',
                    'chat': chat,
                    'receive': receive,
                }
            )

            

            
            # context = {
            #     'user': send,
            #     'chat': chat,
            # }
            return redirect('chat', id=id)
        

    return render(request,'chat/chat.html',{'sender_message':sender_message,'receiver_message':receiver_message,'receive':receive,'all_message':all_message})

