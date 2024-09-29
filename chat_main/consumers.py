import json
from .models import*
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

User=get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_message(self,data):
        massage=Messages.last_30_messages()
        content={'messages':self.List_Message_To_Json(self,messages)}
        self.send_chat_message(content)
    def new_message(self,data):
        auther=data['form']
        auther_user=User.objects.filter(username=auther)[0]
        message=Messages.objects.create(auther=auther_user,content=data['message'])
        content={'commend':'new_message',
                 'message':self.Message_ToJson(message)}
        return self.send_chat_message(content)         
    command={
        'fetch_message':fetch_message,
        'new_message':new_message
    }

    def List_Message_To_Json(self,messages):
        result=[]
        for message in messages:
            result.append(self.Message_ToJson(message))
        return result   

    def Message_ToJson(self,message):
        return{
            'auther':Messages.auther.username,
            'content':Messages.content,
            'time':str(Messages.time)
        }
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.command[data['command']](self,data)

    def send_chat_message(self,message):    
        message = data["message"]
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))   