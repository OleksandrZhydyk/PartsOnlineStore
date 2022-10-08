from django.core.validators import MinValueValidator
from django.db import models

from cart.models import Cart
from catalogue.validators import part_number_validator


class Part(models.Model):
    part_number = models.CharField(primary_key=True, max_length=50, validators=[part_number_validator])
    part_name = models.CharField(max_length=125, null=True, verbose_name="Part name")
    price = models.FloatField(
        verbose_name="Price",
        validators=[MinValueValidator(limit_value=0.01, message="Price has to be greater then 0.01.")],
    )
    discount_price = models.FloatField(verbose_name="Discount", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, editable=False, verbose_name="Part adding date")
    image = models.ImageField(
        default="profiles_avatars/empty_avatar.png",
        null=True,
        blank=True,
        upload_to="profiles_avatars/%Y/%m/%d/",
        verbose_name="Image",
    )
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name="Remark")
    stock_quantity = models.PositiveIntegerField(default=0, blank=True, null=True)


class MachineModel(models.Model):
    MACHINE_TYPES = (
        (1, "Tractor"),
        (2, "Combine"),
        (3, "Self-propelled sprayer"),
        (4, "Self-propelled forage combine"),
        (5, "Loader"),
    )

    model = models.CharField(max_length=15, verbose_name="Model")
    machine_type = models.IntegerField(choices=MACHINE_TYPES, default=1, verbose_name="Machine type")
    part = models.ManyToManyField(to="catalogue.Part", related_name="machine_model")
