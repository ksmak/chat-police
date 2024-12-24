import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chats.routing import websocket_urlpatterns
from chats.middleware import TokenAuthMiddleWare

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleWare(
            AllowedHostsOriginValidator(
                URLRouter(websocket_urlpatterns),
            )
        ),
    }
)
