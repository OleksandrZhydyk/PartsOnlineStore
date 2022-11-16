from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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


class CartItem(models.Model):
    part = models.ForeignKey("catalogue.Part", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
    )
    cart = models.ForeignKey("Cart", related_name="cart_item", on_delete=models.CASCADE)

    def get_total_by_item(self):
        return self.part.price * self.quantity
