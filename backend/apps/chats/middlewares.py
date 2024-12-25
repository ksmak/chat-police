from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token

User = get_user_model()


@database_sync_to_async
def get_user(token):
    try:
        user = Token.objects.get(key=token).user
    except Exception:
        user = AnonymousUser()

    return user


class CustomAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["user"] = await get_user(scope["query_string"].decode("utf-8"))
        return await self.app(scope, receive, send)
