from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient


class TestAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create(email="admin@test.mail", is_staff=True)
        self.admin.set_password("password")
        self.admin.save()
        self.user = get_user_model().objects.create(email="user@test.mail")
        self.user.set_password("password")
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()
        self.admin.delete()

    # def test_admin_user_access(self):
    #     self.client.force_authenticate(user=self.admin)
    #     response = self.client.get(reverse("users"))
    #     self.assertEqual(response.status_code, HTTP_200_OK)

    def test_user_access(self):
        self.client.force_authenticate(user=self.user)
        part_data = {
            "part_number": "RE789654",
            "part_name": "shaft",
            "price": 10,
        }
        response = self.client.post(reverse("part_create"), part_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_admin_model_create_access(self):
        self.client.force_authenticate(user=self.admin)
        model_data = {
            "model": "W660",
        }
        response = self.client.post(reverse("model_create"), model_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data, {"id": 1, "model": "W660", "machine_type": "Tractor"})
