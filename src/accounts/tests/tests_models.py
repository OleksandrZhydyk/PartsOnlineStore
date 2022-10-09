from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create(email="test@test.mail")
        self.user.set_password("password")
        self.user.save()
        self.admin = get_user_model().objects.create(email="admin@test.mail")
        self.admin.set_password("admin_password")
        self.admin.save()

    def tearDown(self) -> None:
        self.admin.delete()
        self.user.delete()

    def test_user_login_wrong_email(self):
        user_login = self.client.login(email="wrong@email.mail", password="password")
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(email="test@test.mail", password="wrong_password")
        self.assertFalse(user_login)

    # def test_user_access(self):
    #     self.client.force_login(self.user)
    #     response = self.client.get(reverse("admin"))
    #     self.assertEqual(response, HTTPStatus.OK)

    # def test_admin_access_to_admin_panel(self):
    #     self.client.force_login(self.admin)
    #     response = self.client.get(reverse("admin:index"))
    #     self.assertEqual(response, HTTPStatus.OK)
