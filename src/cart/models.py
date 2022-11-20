from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from catalogue.validators import part_number_validator


class Cart(models.Model):

    PAYMENT_TYPES = (
        (1, "GooglePay"),
        (2, "Visa"),
        (3, "Cash"),
    )

    DELIVERY_SERVICES = (
        (1, "Nova Poshta"),
        (2, "Meest Express"),
        (3, "Ukrposhta"),
        (4, "Self-delivery"),
    )

    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.IntegerField(choices=PAYMENT_TYPES, default=1)
    order_id = models.CharField(max_length=100, null=True, default="")
    ordered = models.BooleanField(default=False)
    delivery_service = models.IntegerField(choices=DELIVERY_SERVICES, default=1)
    phone_number = PhoneNumberField(blank=False, null=True)
    contact_name = models.CharField(max_length=100, null=True, blank=False)
    contact_surname = models.CharField(max_length=100, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    total_amount = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.order_id)


class CartItem(models.Model):
    part = models.ForeignKey("catalogue.Part", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
    )
    cart = models.ForeignKey("Cart", related_name="cart_item", on_delete=models.CASCADE)
    part_number = models.CharField(max_length=50, validators=[part_number_validator], null=True)
    part_name = models.CharField(max_length=125, null=True, verbose_name="Part name")
    price = models.FloatField(
        verbose_name="Price",
        validators=[MinValueValidator(limit_value=0.01, message="Price has to be greater then 0.01.")],
    )
    discount = models.FloatField(
        verbose_name="Discount",
        blank=True,
        null=True,
        validators=[MinValueValidator(limit_value=0.01), MaxValueValidator(limit_value=1)],
        default=1,
    )

    def get_total_by_item(self):
        return round(self.price * self.discount * self.quantity, 2)

    def __str__(self):
        return str(self.part_number)
