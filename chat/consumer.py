from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *
from channels.db import database_sync_to_async

# ChatConsumer extends the AsyncWebsocketConsumer Class.
# The AsyncWebsocketConsumer Class is used to make our asynchronous consumer.
class ChatConsumer(AsyncWebsocketConsumer):

    # All the functions will take a defualt parameter of self.
    # Since the functions are defined in the async class all of its functions will use the async keyword.
    
    async def connect(self):
        # scope is a set of key/value pairs which contain the information about the current connection and its environment.
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()
        
    # This handler is called when data is received from the client.
    # The receive method is automatically called by Django Channels whenever a message is received on the WebSocket. 
    # The message sent by the client is provided as the text_data argument.
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        print(data_json)
        
        event = {
            "type": "send_message",
            "message": data_json
        }
        
        await self.channel_layer.group_send(self.room_name, event)    
            
    # This handler is called when either the client connection is lost, either the client closes the connection, or
    # the server losing the connection, or the loss of the socket.
    # code parameter is an integer that indicates the reason for disconnection (such as normal closure, error, etc.).
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close(code)
        

    # the event dict is coming from the receive function.
    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data=data)
        
        response = {
            "sender":data["sender"],
            "message":data["message"],
        }
        
        await self.send(text_data=json.dumps({"message":response}))
    
    # converts django's ORM methods(get, filter, etc) to async. They are synchronous by nature.
    @database_sync_to_async
    def create_message(self, data):
        
        get_room = Room.objects.get(room_name=data['room_name'])        
        new_message = Message.objects.create(room = get_room, message=data['message'], sender=data["sender"])
        return new_message

        # if the same user sends an existing message again then it will not be sent
        # only new messages will be sent
        # if  Message.objects.filter(message=data['message'], sender=data["sender"]).exists():
        #     new_message = Message.objects.create(room = get_room,
        #     message=data['message'], sender=data["sender"])