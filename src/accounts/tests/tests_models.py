from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create(email="test@test.mail")
        self.user.set_password("password")
        self.admin = get_user_model().objects.create(email="admin@test.mail")
        self.admin.set_password("admin_password")

    def tearDown(self) -> None:
        self.admin.delete()
        self.user.delete()

    def test_user_login_wrong_email(self):
        user_login = self.client.login(email="wrong@email.mail", password="password")
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(email="test@test.mail", password="wrong_password")
        self.assertFalse(user_login)
