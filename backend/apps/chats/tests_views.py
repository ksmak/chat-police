from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from auths.models import CustomUser
from .models import Chat, Message
from unittest.mock import ANY


class ChatViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="Zz@12345", email="user@mail.ru"
        )
        self.user.save()

        self.seconduser = CustomUser.objects.create_user(
            username="testseconduser", password="Zz@12345", email="seconduser@mail.ru"
        )
        self.seconduser.save()

        self.chat = Chat.objects.create(title="test chat")
        self.chat.users.set([self.user, self.seconduser])
        self.chat.actives.set([self.user, self.seconduser])
        self.chat.save()

        self.message = Message.objects.create(
            from_user=self.user,
            to_chat=self.chat,
            text="Hello!",
        )
        self.message.save()

    def tearDown(self):
        self.user.delete()

    def test_without_auth(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(path="/api/chats/", data={}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.client.get("/api/chats/", format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.client.post(path="/api/uploadfile/", format="multipart")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_chat(self):
        self.client.force_authenticate(user=self.user)

        expected_data = [
            {
                "id": ANY,
                "title": self.chat.title,
                "users": [self.seconduser.id, self.user.id],
                "actives": [self.seconduser.id, self.user.id],
                "created_at": ANY,
                "messages": [
                    {
                        "id": ANY,
                        "state": self.message.state,
                        "from_user": self.message.from_user.id,
                        "to_user": None,
                        "to_chat": self.message.to_chat.id,
                        "text": self.message.text,
                        "file": self.message.file,
                        "created_at": ANY,
                        "changed_at": ANY,
                        "deleted_at": ANY,
                        "readers": [],
                        "fullname": self.message.from_user.full_name,
                    }
                ],
            }
        ]

        response = self.client.get("/api/chats/")
        assert response.status_code == status.HTTP_200_OK
        self.assertListEqual(expected_data, response.data)
