from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class Cart(models.Model):
    PAYMENT_TYPES = (
        (1, "GooglePay"),
        (2, "Visa"),
        (3, "PayPal"),
    )

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPES, default="Visa")
    payment_id = models.CharField(max_length=100, null=True)
    ordered = models.BooleanField(default=False)


class CartItem(models.Model):
    part = models.ForeignKey("catalogue.Part", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
    )
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)

    def get_price_by_part(self):
        return self.part.price * self.quantity


class OrdersHistory(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart, related_name="orders_history", on_delete=models.CASCADE)
