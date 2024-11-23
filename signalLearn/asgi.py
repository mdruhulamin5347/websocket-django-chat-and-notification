"""
ASGI config for signalLearn project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Home.routing import websocket_urlpatterns   
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signalLearn.settings')  # Replace with your project name

# ASGI application
application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # HTTP handling
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns   # WebSocket routing
            )
        ),
    ),
})






