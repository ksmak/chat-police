from django.test import TestCase
from django.contrib.auth import authenticate

from .models import CustomUser


class UserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="Zz@12345", email="testuser@mail.ru"
        )

    def tearDown(self):
        self.user.delete()

    def test_correct_user(self):
        user = authenticate(username="testuser", password="Zz@12345")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username="wronguser", password="Zz@12345")
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username="testuser", password="wrongpass")
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_user_fullname(self):
        self.assertEqual(f"{self.user.username}", self.user.full_name)
        self.user.first_name = "FirstName"
        self.user.last_name = "LastName"
        self.user.save()
        self.assertEqual(
            f"{self.user.last_name} {self.user.first_name}", self.user.full_name
        )
        self.user.first_name = "FirstName"
        self.user.last_name = ""
        self.user.save()
        self.assertEqual(f"{self.user.first_name}", self.user.full_name)
        self.user.first_name = ""
        self.user.last_name = "LastName"
        self.user.save()
        self.assertEqual(f"{self.user.last_name}", self.user.full_name)
