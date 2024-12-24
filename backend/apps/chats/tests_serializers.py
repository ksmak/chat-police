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
            username="testuser1", password="Zz@12345", email="testuser1@mail.ru"
        )
        self.user1.first_name = "Ахмет"
        self.user1.last_name = "Ахметов"
        self.user1.save()

        self.user2 = CustomUser.objects.create_user(
            username="testuser2", password="Zz@12345", email="testuser2@mail.ru"
        )
        self.user2.first_name = "Самат"
        self.user2.last_name = "Саматов"
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
        self.message1.delete()
        self.message2.delete()
        self.message3.delete()
        self.chat.delete()
        self.user1.delete()
        self.user2.delete()

    def test_reader_serializer(self):
        serializer = ReaderSerializer(self.reader)
        test_data = {
            "id": ANY,
            "message": self.message1.id,
            "user": self.user2.id,
            "fullname": self.user2.full_name,
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
                    "id": ANY,
                    "message": self.message1.id,
                    "user": self.user2.id,
                    "fullname": self.user2.full_name,
                    "read_date": ANY,
                }
            ],
            "fullname": self.user1.full_name,
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
                    "file": self.message3.file,
                    "created_at": ANY,
                    "changed_at": ANY,
                    "deleted_at": ANY,
                    "readers": [],
                    "fullname": self.message3.from_user.full_name,
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
