from django.test import TestCase
from unittest.mock import ANY

from .models import CustomUser
from .serializers import CustomUserSerializer
from chats.models import Chat, Message


class UserSerializerTest(TestCase):
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

    def tearDown(self):
        self.message1.delete()
        self.message2.delete()
        self.message3.delete()
        self.chat.delete()
        self.user1.delete()
        self.user2.delete()

    def test_user_serializer(self):
        message1 = {
            "id": self.message1.id,
            "state": self.message1.state,
            "from_user": self.user1.id,
            "to_user": self.user2.id,
            "to_chat": None,
            "text": self.message1.text,
            "file": None,
            "created_at": ANY,
            "changed_at": ANY,
            "deleted_at": ANY,
            "readers": [],
            "fullname": self.user1.full_name,
        }

        message2 = {
            "id": self.message2.id,
            "state": self.message2.state,
            "from_user": self.user2.id,
            "to_user": self.user1.id,
            "to_chat": None,
            "text": self.message2.text,
            "file": None,
            "created_at": ANY,
            "changed_at": ANY,
            "deleted_at": ANY,
            "readers": [],
            "fullname": self.user2.full_name,
        }

        serializer1 = CustomUserSerializer(self.user1)
        test_data1 = {
            "id": self.user1.id,
            "username": self.user1.username,
            "full_name": self.user1.full_name,
            "is_active": self.user1.is_active,
            "messages": [message1, message2],
            "online": None,
        }
        self.assertDictEqual(serializer1.data, test_data1)

        serializer2 = CustomUserSerializer(self.user2)
        test_data2 = {
            "id": self.user2.id,
            "username": self.user2.username,
            "full_name": self.user2.full_name,
            "is_active": self.user2.is_active,
            "messages": [message1, message2],
            "online": None,
        }
        self.assertDictEqual(serializer2.data, test_data2)