from django.test import TestCase
from unittest.mock import ANY

from auths.models import CustomUser
from .models import Chat, Message, Reader, OnlineUser
from .serializers import (
    ReaderSerializer,
    MessageSerializer,
    ChatSerializer,
    OnlineUserSerializer,
)


class ChatSerializerTest(TestCase):
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
            text="Hello Самат!",
        )
        self.message1.save()

        self.message2 = Message.objects.create(
            from_user=self.user2,
            to_user=self.user1,
            text="Hi Ахмет!",
        )
        self.message2.save()

        self.message3 = Message.objects.create(
            from_user=self.user1,
            to_chat=self.chat,
            text="Всем привет!",
        )
        self.message3.save()

        self.reader = Reader(message=self.message1, user=self.user2)
        self.reader.save()

        self.online_user = OnlineUser(user=self.user1, is_active=True)
        self.online_user.save()

    def tearDown(self):
        self.chat.delete()
        self.user1.delete()
        self.user2.delete()

    def test_reader_serializer(self):
        serializer = ReaderSerializer(self.reader)
        test_data = {
            "user": self.user2.id,
            "name": self.user2.name,
            "read_date": ANY,
        }
        self.assertDictEqual(serializer.data, test_data)

    def test_message_serializer(self):
        serializer = MessageSerializer(self.message1)
        test_data = {
            "id": ANY,
            "state": self.message1.state,
            "from_user": self.user1.id,
            "to_user": self.user2.id,
            "to_chat": None,
            "text": self.message1.text,
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
        }
        self.assertDictEqual(serializer.data, test_data)

    def test_chat_serializer(self):
        serializer = ChatSerializer(self.chat)
        test_data = {
            "id": ANY,
            "title": self.chat.title,
            "users": [self.user1.id, self.user2.id],
            "actives": [self.user1.id, self.user2.id],
            "created_at": ANY,
            "messages": [
                {
                    "id": ANY,
                    "state": self.message3.state,
                    "from_user": self.message3.from_user.id,
                    "to_user": None,
                    "to_chat": self.message3.to_chat.id,
                    "text": self.message3.text,
                    "file": None,
                    "created_at": ANY,
                    "changed_at": ANY,
                    "deleted_at": ANY,
                    "readers": [],
                    "name": self.message3.from_user.name,
                }
            ],
        }
        self.assertDictEqual(serializer.data, test_data)

    def test_online_user_serializer(self):
        serializer = OnlineUserSerializer(self.online_user)
        test_data = {
            "user": self.online_user.user.id,
            "is_active": self.online_user.is_active,
            "last_date": ANY,
        }
        self.assertDictEqual(serializer.data, test_data)
