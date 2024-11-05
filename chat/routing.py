from django.urls import path
from .consumer import ChatConsumer

# for websockets connections  routing
wsPattern = [
    # when routing our consumers we use the as_asgi() method, The ChatConsumer is also defined in the consumer.py
    path("ws/messages/<str:room_name>/", ChatConsumer.as_asgi())
]