from django.db import models

from cart.models import Cart
from core.models import Shop


class Part(models.Model):
    part_number = models.CharField(primary_key=True, max_length=50)
    part_name = models.CharField(max_length=125, null=True)
    price = models.FloatField(verbose_name="Price")
    discount_price = models.FloatField(verbose_name="Discount", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, editable=False, verbose_name="Part adding date")
    image = models.ImageField(default='profiles_avatars/empty_avatar.png', null=True,
                              blank=True, upload_to="profiles_avatars/%Y/%m/%d/", verbose_name="Image")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name="Remark")
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)


class MachineModel(models.Model):

    MACHINE_TYPES = (
        (1, "Tractor"),
        (2, "Combine"),
        (3, "Self-propelled sprayer"),
        (4, "Self-propelled forage combine"),
        (5, "Loader"))

    model = models.CharField(max_length=15, verbose_name="Model")
    machine_type = models.CharField(max_length=50, choices=MACHINE_TYPES,
                                    default="Please choose a machine type",
                                    verbose_name="Machine type")
    part = models.ManyToManyField(to='catalogue.Part')
