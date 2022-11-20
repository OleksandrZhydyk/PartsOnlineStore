from django.db import models
from location_field.models.plain import PlainLocationField

from catalogue.models import Part


class Shop(models.Model):
    address = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=["address"], zoom=7, null=True)
    part = models.ManyToManyField(to=Part, related_name="shop", null=True)

    def __str__(self):
        return str(self.address)
