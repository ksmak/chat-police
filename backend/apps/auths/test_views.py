from django.test import TestCase
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
    force_authenticate,
)

from .models import CustomUser
from .serializers import CustomUserSerializer
from .views import UsersViewSet


class UserViewSetTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser1", password="Zz@12345", email="testuser1@mail.ru"
        )
        self.user1.save()
        self.user2 = CustomUser.objects.create_user(
            username="testuser2", password="Zz@12345", email="testuser2@mail.ru"
        )
        self.user2.save()
        self.superuser = CustomUser.objects.create_superuser(
            username="testsuperuser", password="Zz@12345", email="testsuperuser@mail.ru"
        )
        self.superuser.save()
        self.factory = APIRequestFactory()
        self.view = UsersViewSet.as_view({"get": "list"})

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.superuser.delete()

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
