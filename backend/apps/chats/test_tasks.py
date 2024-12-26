from django.test import TestCase
from unittest.mock import ANY
from django.test.utils import override_settings
import pytest

from .tasks import (
    update_chat,
    create_message,
    read_message,
    edit_message,
    delete_message,
    clean_chat,
)
from auths.models import CustomUser
from .models import Chat, Message


@pytest.mark.celery(result_backend="redis://")
class TestCeleryTasks(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser1", ip="192.168.100.1", name="testuser1", password="12345"
        )
        self.user1.save()

        self.user2 = CustomUser.objects.create_user(
            username="testuser2", ip="192.168.100.2", name="testuser2", password="12345"
        )
        self.user2.save()

        self.chat = Chat.objects.create(
            title="TestChat",
        )
        self.chat.users.set([self.user1, self.user2])
        self.chat.actives.set([self.user1, self.user2])
        self.chat.save()

        self.message1 = Message.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            text="Hello user!",
        )
        self.message1.save()

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_update_chat(self):
        result = update_chat.delay(from_id=self.user1.id, is_active=True)
        self.assertTrue(result.successful())
        self.assertDictEqual(
            result.get(),
            {
                "type": "chat_message",
                "category": "change_chat",
                "online_user": {
                    "user": self.user1.id,
                    "is_active": True,
                    "last_date": ANY,
                },
            },
        )

        result = update_chat.delay(from_id=self.user2.id, is_active=False)
        self.assertTrue(result.successful())
        self.assertDictEqual(
            result.get(),
            {
                "type": "chat_message",
                "category": "change_chat",
                "online_user": {
                    "user": self.user2.id,
                    "is_active": False,
                    "last_date": ANY,
                },
            },
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_user_message(self):
        result = create_message.delay(
            message_type="user",
            from_id=self.user1.id,
            to_id=self.user2.id,
            text="test message...",
            file="filename",
        )
        self.assertTrue(result.successful())
        self.assertDictEqual(
            result.get(),
            {
                "type": "chat_message",
                "category": "new_message",
                "message_type": "user",
                "message": {
                    "id": ANY,
                    "state": 1,
                    "from_user": self.user1.id,
                    "to_user": self.user2.id,
                    "to_chat": None,
                    "text": "test message...",
                    "file": "/media/filename",
                    "created_at": ANY,
                    "changed_at": ANY,
                    "deleted_at": ANY,
                    "readers": [],
                    "name": self.user1.name,
                },
            },
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_chat_message(self):
        result = create_message.delay(
            message_type="chat",
            from_id=self.user1.id,
            to_id=self.chat.id,
            text="test message...",
            file="filename",
        )
        self.assertTrue(result.successful())
        self.assertDictEqual(
            result.get(),
            {
                "type": "chat_message",
                "category": "new_message",
                "message_type": "chat",
                "message": {
                    "id": ANY,
                    "state": 1,
                    "from_user": self.user1.id,
                    "to_user": None,
                    "to_chat": self.chat.id,
                    "text": "test message...",
                    "file": "/media/filename",
                    "created_at": ANY,
                    "changed_at": ANY,
                    "deleted_at": ANY,
                    "readers": [],
                    "name": self.user1.name,
                },
            },
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_read_message(self):
        result = read_message.delay(
            message_type="user",
            from_id=self.user2.id,
            message_id=self.message1.id,
        )
        self.assertTrue(result.successful())
        self.assertDictEqual(
            result.get(),
            {
                "type": "chat_message",
                "category": "change_message",
                "message_type": "user",
                "message": {
                    "id": ANY,
                    "state": 1,
                    "from_user": self.user1.id,
                    "to_user": self.user2.id,
                    "to_chat": None,
                    "text": "Hello user!",
                    "file": None,
                    "created_at": ANY,
                    "changed_at": ANY,
                    "deleted_at": ANY,
                    "readers": [
                        {
                            "user": self.user2.id,
                            "name": self.user2.name,
                            "read_date": ANY,
                        }
                    ],
                    "name": self.user1.name,
                },
            },
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_edit_message(self):
        result = edit_message.delay(
            message_type="user",
            from_id=self.user1.id,
            text="another text...",
            message_id=self.message1.id,
        )
        self.assertTrue(result.successful())
        self.assertDictEqual(
            result.get(),
            {
                "type": "chat_message",
                "category": "change_message",
                "message_type": "user",
                "message": {
                    "id": ANY,
                    "state": 1,
                    "from_user": self.user1.id,
                    "to_user": self.user2.id,
                    "to_chat": None,
                    "text": "another text...",
                    "file": None,
                    "created_at": ANY,
                    "changed_at": ANY,
                    "deleted_at": ANY,
                    "readers": ANY,
                    "name": self.user1.name,
                },
            },
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_edit_message(self):
        result = delete_message.delay(
            message_type="user",
            from_id=self.user1.id,
            message_id=self.message1.id,
        )
        self.assertTrue(result.successful())
        self.assertDictEqual(
            result.get(),
            {
                "type": "chat_message",
                "category": "change_message",
                "message_type": "user",
                "message": {
                    "id": ANY,
                    "state": 2,
                    "from_user": self.user1.id,
                    "to_user": self.user2.id,
                    "to_chat": None,
                    "text": ANY,
                    "file": ANY,
                    "created_at": ANY,
                    "changed_at": ANY,
                    "deleted_at": ANY,
                    "readers": ANY,
                    "name": self.user1.name,
                },
            },
        )
