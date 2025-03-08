import json
from authapp.utils import send_reset_password_email
from .models import Message, Conversation
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.room_name}'
        user_id= self.scope['user_id']
        print(f'user_id: {user_id}')
        self.user=await self.get_user(user_id)
        print(self.user)
        
        

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        if not message:
            return

        # Save message to the database
        await self.save_message(self.user, self.room_name, message)

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': self.user.id,
        }))

    @database_sync_to_async
    def save_message(self, sender, conversation_id, content):
        """
        This function remains synchronous because Django ORM is not async,
        so it uses @database_sync_to_async.
        """
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            Message.objects.create(
                sender=sender,
                conversation=conversation,
                content=content
            )
        except Conversation.DoesNotExist:
            pass

    @database_sync_to_async
    def get_user(self, user_id):
        """
        This function is also synchronous and wrapped with @database_sync_to_async.
        """
        try:
            User = get_user_model()
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
