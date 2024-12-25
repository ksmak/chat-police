from django.test import TestCase
from django.urls import path
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from channels.security.websocket import AllowedHostsOriginValidator
from rest_framework.authtoken.models import Token

from auths.models import CustomUser
from settings.asgi import application


class TestConsumer(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser1", ip="127.0.0.1", name="testuser1", password="12345"
        )
        self.user1.save()
        self.token = Token.objects.create(user=self.user1).key
        self.user2 = CustomUser.objects.create_user(
            username="testuser2", ip="192.168.100.2", name="testuser2", password="12345"
        )
        self.user2.save()

    async def test_chat_consumer(self):
        communicator = WebsocketCommunicator(application, f"/ws/chat?{self.token}")
        connected, _ = await communicator.connect()
        assert connected
        # new message
        await communicator.send_json_to(
            {
                "message": "send_new",
                "message_type": "user",
                "to_id": self.user2.id,
                "text": "test message...",
                "file": None,
            }
        )
        # response = await communicator.receive_json_from()
        # assert response == {}
        # Close
        await communicator.disconnect()
