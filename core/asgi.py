import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Ensure settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import your WebSocket routing
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack( # Apply authentication to WebSocket connections
        URLRouter(
            chat.routing.websocket_urlpatterns # Your WebSocket URLs
        )
    ),
})