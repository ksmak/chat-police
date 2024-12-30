import pytest
from django.test import TestCase
from django.test.utils import override_settings
from channels.testing import WebsocketCommunicator

from auths.models import CustomUser
from chats.models import Message
from chats.consumers import ChatConsumer


@pytest.mark.celery(result_backend="redis://")
class TestChatConsumer(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            ip="127.0.0.1", name="testuser1", username="testuser1", password="12345"
        )
        self.user1.save()

        self.user2 = CustomUser.objects.create(
            ip="192.168.100.2", name="testuser2", username="testuser2", password="12345"
        )
        self.user2.save()

        self.message = Message.objects.create(
            from_user=self.user2,
            to_user=self.user1,
            text="Hello!",
        )
        self.message.save()

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    async def test_chat_consumer(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/testws/")
        communicator.scope["user"] = self.user1
        connected, _ = await communicator.connect()
        assert connected
        # create message
        await communicator.send_json_to(
            {
                "message": "send_new",
                "message_type": "user",
                "to_id": self.user1.id,
                "text": "test message...",
                "file": None,
            }
        )
        response = await communicator.receive_json_from(timeout=5)
        self.assertDictEqual(response, {"message": "creating message..."})
        # read message
        await communicator.send_json_to(
            {
                "message": "send_read",
                "message_type": "user",
                "message_id": self.message.id,
            }
        )
        response = await communicator.receive_json_from(timeout=5)
        self.assertDictEqual(response, {"message": "reading message..."})
        # edit message
        await communicator.send_json_to(
            {
                "message": "send_edit",
                "message_type": "user",
                "text": "something...",
                "message_id": self.message.id,
            }
        )
        response = await communicator.receive_json_from(timeout=5)
        self.assertDictEqual(response, {"message": "editing message..."})
        # delete message
        await communicator.send_json_to(
            {
                "message": "send_delete",
                "message_type": "user",
                "message_id": self.message.id,
            }
        )
        response = await communicator.receive_json_from(timeout=5)
        self.assertDictEqual(response, {"message": "deleting message..."})
        # close
        await communicator.disconnect()
