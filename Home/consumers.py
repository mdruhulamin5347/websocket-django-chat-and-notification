import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_list_or_404
from .models import Chat
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.group_name = 'notifications'

        # Add this channel to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # async def receive(self,text_data):
        
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        # if message:
        #     # Send message to the group
        #     await self.channel_layer.group_send(
        #         self.group_name,
        #         {
        #             'type': 'send_notification',
        #             'message': message
        #         }
        #     )

    async def send_notification(self, event):
    # Check that message and username are present in the event
        message = event.get('message', 'No message')  # Default message if not provided
        username = event.get('username', 'Anonymous')  # Default username if not provided

        # Send the message and username as JSON to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))




import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string
from channels.layers import get_channel_layer

class RealTimeChatApp(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        # self.receive_id = self.scope['url_route']['kwargs']['receive_id']
        # self.room_group_name = f"chat_{self.receive_id}"
        self.room_group_name = "chat_room_group"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"{self.user.username} connected to chat room: {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"{self.user.username} disconnected from chat room: {self.room_group_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        receiver_username = data.get('receiver', '')  

        


        try:
            receiver = await database_sync_to_async(User.objects.get)(username=receiver_username)
        except User.DoesNotExist:
            print("Receiver does not exist")
            return

        # Send the chat message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_chat_message',
                'chat': message,
                'receive': self.user.username,  # Send the username of the sender
            }
        )
    
        # Save the message to the database
        chat_message = Chat(sender=self.user, receiver=receiver, message=message)
        await database_sync_to_async(chat_message.save)()


    async def send_chat_message(self, event):
        chat = event.get('chat', 'No chat')
        receive = event.get('receive', 'Anonymous')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'chat': chat,
            'receive': receive,
        }))

