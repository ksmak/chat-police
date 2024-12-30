from django.test import TestCase
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
    force_authenticate,
)
from unittest.mock import ANY

from auths.models import CustomUser
from auths.serializers import CustomUserSerializer
from auths.views import UsersViewSet, CustomAuthToken


class UserViewSetTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser1", ip="127.0.0.1", name="testuser1", password="12345"
        )
        self.user1.save()
        self.user2 = CustomUser.objects.create_user(
            username="testuser2", ip="192.168.100.2", name="testuser2", password="12345"
        )
        self.user2.save()
        self.superuser = CustomUser.objects.create_superuser(
            username="testsuperuser",
            ip="192.168.100.3",
            name="testsuperuser",
            password="Zz@12345",
        )
        self.superuser.save()
        self.factory = APIRequestFactory()
        self.token_view = CustomAuthToken.as_view()
        self.view = UsersViewSet.as_view({"get": "list"})

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.superuser.delete()

    def test_get_token(self):
        request = self.factory.post("/api/token/")
        response = self.token_view(request)
        except_data = {
            "token": ANY,
            "user_name": "testuser1",
        }
        self.assertDictEqual(response.data, except_data)

    def test_list_without_authenticate(self):
        request = self.factory.get("/api/users/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_with_authenticate(self):
        request = self.factory.get("/api/users/")
        force_authenticate(request, user=self.user1)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CustomUserSerializer([self.user2], many=True)
        self.assertListEqual(serializer.data, response.data)
