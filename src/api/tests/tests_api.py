from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient

from cart.models import OrdersHistory
from catalogue.models import MachineModel, Part
from core.models import Shop


class TestAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create(email="admin@test.mail", is_staff=True)
        self.admin.set_password("password")
        self.user = get_user_model().objects.create(email="user@test.mail")
        self.user.set_password("password")

    def tearDown(self) -> None:
        self.user.delete()
        self.admin.delete()

    def test_user_shops_retrieve(self):
        self.client.force_authenticate(user=self.user)
        self.shop = Shop.objects.create(
            address="вулиця Глінки, 2, Дніпро, Дніпропетровська область, 49000",
            location="48.4660662,35.051501",
        )
        response = self.client.get(reverse("shops_list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "id": 1,
                    "address": "вулиця Глінки, 2, Дніпро, Дніпропетровська область, 49000",
                    "part": [],
                    "location": "48.4660662,35.051501",
                }
            ],
        )

    def test_user_part_create_access(self):
        self.client.force_authenticate(user=self.user)
        part_data = {
            "part_number": "RE789654",
            "part_name": "shaft",
            "price": 10,
        }
        response = self.client.post(reverse("part_create"), part_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_admin_model_create(self):
        self.client.force_authenticate(user=self.admin)
        model_data = {
            "model": "W660",
        }
        response = self.client.post(reverse("model_create"), model_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data, {"id": 1, "model": "W660", "machine_type": "Tractor"})

    def test_admin_model_delete(self):
        self.client.force_authenticate(user=self.admin)
        MachineModel.objects.create(model="W660")
        MachineModel.objects.create(model="6155M")
        self.client.delete(reverse("model_delete", kwargs={"model": "6155M"}))
        response = self.client.get(reverse("models_retrieve"))
        self.assertEqual(response.data, [{"id": response.data[0]["id"], "model": "W660", "machine_type": "Tractor"}])

    def test_admin_part_patch(self):
        self.client.force_authenticate(user=self.admin)
        part_data = {"part_number": "RE789654", "part_name": "shaft", "price": 10, "description": "crankshaft"}
        Part.objects.create(**part_data)
        part_data_updated = {"part_name": "sprocket", "price": 7.5}
        response = self.client.patch(reverse("part_update", kwargs={"part_number": "RE789654"}), part_data_updated)
        self.assertEqual(response.data["part_name"], "sprocket")
        self.assertEqual(response.data["price"], 7.5)

    def test_user_to_foreign_user_profile_access(self):
        self.strange_user = get_user_model().objects.create(email="strange_user@test.mail")
        self.strange_user.set_password("password")
        self.strange_user.save()
        self.client.force_authenticate(user=self.strange_user)
        response = self.client.get(reverse("profile_retrieve", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_to_foreign_user_orders_history_access(self):
        OrdersHistory.objects.create(user=self.user)
        self.strange_user = get_user_model().objects.create(email="strange_user@test.mail")
        self.strange_user.set_password("password")
        self.client.force_authenticate(user=self.strange_user)
        response = self.client.get(reverse("orders_history_retrieve", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
