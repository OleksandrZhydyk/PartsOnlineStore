from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from cart.models import Cart, CartItem
from catalogue.models import Part


class TestCartItemModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email="test@test.com", password="self.user")
        self.user.save()
        self.cart = Cart.objects.create(user=self.user)
        self.cart.save()
        self.part = Part.objects.create(part_number="test", part_name="test", price=100.99)
        self.part.save()
        self.cart_item = CartItem.objects.create(part=self.part, cart=self.cart, quantity=2)
        self.cart_item.save()

    def tearDown(self):
        self.user.delete()
        self.cart.delete()
        self.part.delete()
        self.cart_item.delete()

    def test_cart_item_attrs(self):
        self.assertTrue(isinstance(self.cart, Cart))
        self.assertTrue(isinstance(self.part, Part))
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.part.part_name, "test")

    def test_update_cart_item_attrs(self):
        self.cart_item.quantity = 5
        self.part.save()
        self.assertEqual(self.cart_item.quantity, 5)

    def test_price_by_item(self):
        self.assertEqual(self.cart_item.get_price_by_part(), 201.98)

    def test_cart_item_error(self):

        with transaction.atomic():
            invalid_quantity = -1
            self.assertRaises(
                IntegrityError,
                CartItem.objects.create,
                **{"part": self.part, "cart": self.cart, "quantity": invalid_quantity},
            )
