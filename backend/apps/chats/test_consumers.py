import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from auths.models import CustomUser
from .consumers import ChatConsumer
from chats.tasks import (
    update_chat,
    create_message,
)

TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        "CONFIG": {"capacity": 1000, "expiry": 10},
    },
}


@database_sync_to_async
def create_user():
    user = CustomUser.objects.create(
        ip="127.0.0.1", name="testuser", username="testuser", password="12345"
    )
    return user


# @pytest.fixture(autouse=True)
# def mock_celery_tasks(monkeypatch):
#     monkeypatch.setattr(update_chat, "delay", lambda *args, **kwargs: None)
#     monkeypatch.setattr(create_message, "delay", lambda *args, **kwargs: None)


# @pytest.fixture(autouse=True)
# def mocked_update_chat(mocker):
#     # Mock the Celery task
#     return mocker.patch("chats.tasks.update_chat.delay", return_value={})


# @pytest.fixture(autouse=True)
# def mocked_create_message(mocker):
#     # Mock the Celery task
#     return mocker.patch("chats.tasks.create_message.delay", return_value={})


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestChatConsumer:
    async def test_chat_consumer(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        self.user = await create_user()

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/testws/")
        communicator.scope["user"] = self.user
        connected, _ = await communicator.connect()
        assert connected
        # new message
        await communicator.send_json_to(
            {
                "message": "send_new123",
                "message_type": "user",
                "to_id": self.user.id,
                "text": "test message...",
                "file": None,
            }
        )
        # response = await communicator.receive_from(timeout=5)
        # assert response == {"status": "success", "text": "Hello, world!"}
        # Close
        await communicator.disconnect()
