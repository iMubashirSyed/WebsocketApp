"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# ProtocolTypeRouter helps route different types of connections (like HTTP and WebSocket).
# URLRouter is used to define WebSocket URL routing patterns.
from channels.routing import ProtocolTypeRouter, URLRouter
from  chat.routing import wsPattern

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Calls get_asgi_application() to create an ASGI application instance for handling standard HTTP requests.
http_response_app = get_asgi_application()

application = ProtocolTypeRouter(
    {"http": http_response_app, "websocket": URLRouter(wsPattern)} # wsPattern is the list of urls defined in the routing.py
    # http requests go to http_response_app to handle typical Django HTTP views.
)