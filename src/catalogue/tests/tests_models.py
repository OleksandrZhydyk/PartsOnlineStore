from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from catalogue.models import MachineModel, Part


class TestPartModel(TestCase):
    def setUp(self):
        self.part = Part.objects.create(part_number="RE12345", part_name="test", price=100.99)
        self.part.save()

    def tearDown(self):
        self.part.delete()

    def test_read_part_attrs(self):
        self.assertEqual(self.part.part_number, "RE12345")
        self.assertEqual(self.part.part_name, "test")
        self.assertEqual(self.part.price, 100.99)

    def test_update_part_attrs(self):
        self.part.part_number = "RE123451"
        self.part.price = 99.99
        self.part.save()
        self.assertEqual(self.part.part_number, "RE123451")
        self.assertEqual(self.part.price, 99.99)

    def test_part_duplicate_error(self):

        with transaction.atomic():
            self.assertRaises(
                IntegrityError, Part.objects.create, **{"part_number": "RE12345", "part_name": "test", "price": 100.99}
            )

    def test_part_error(self):
        with self.assertRaises(ValidationError):
            invalid_part_number = "test"
            self.part.part_number = invalid_part_number
            self.part.full_clean()

        with self.assertRaises(ValidationError):
            invalid_part_number = "Test"
            self.part.part_number = invalid_part_number
            self.part.full_clean()

        with self.assertRaises(ValidationError):
            invalid_part_number = "A123"
            self.part.part_number = invalid_part_number
            self.part.full_clean()

        with self.assertRaises(ValidationError):
            invalid_part_number = "12345"
            self.part.part_number = invalid_part_number
            self.part.full_clean()

        with self.assertRaises(ValidationError):
            invalid_price = 0
            self.part.price = invalid_price
            self.part.full_clean()


class TestMachineModel(TestCase):
    def setUp(self):
        self.part = Part.objects.create(part_number="test", part_name="test", price=100.99)
        self.part.save()
        self.machine_model = MachineModel.objects.create(model="8335R", machine_type=1)
        self.machine_model.part.set((self.part,))
        self.machine_model.save()

    def tearDown(self):
        self.part.delete()
        self.machine_model.delete()

    def test_read_machine_model_attrs(self):
        self.assertTrue(isinstance(MachineModel.objects.first().part.first(), Part))
        self.assertEqual(self.machine_model.model, "8335R")
        self.assertEqual(self.machine_model.machine_type, 1)

    def test_update_machine_model_attrs(self):
        self.machine_model.model = "S770"
        self.machine_model.machine_type = 2
        self.part.save()
        self.assertEqual(self.machine_model.model, "S770")
        self.assertEqual(self.machine_model.machine_type, 2)
