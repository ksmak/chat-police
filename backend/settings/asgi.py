import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chats.middlewares import CustomAuthMiddleware
from chats.consumers import ChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            CustomAuthMiddleware(
                URLRouter(
                    [
                        path("ws/chat", ChatConsumer.as_asgi()),
                    ]
                ),
            )
        ),
    }
)
