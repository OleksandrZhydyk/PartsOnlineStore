from django.db import models

from catalogue.models import Part


class Shop(models.Model):
    address = models.CharField(max_length=255)
    part = models.ManyToManyField(to=Part, related_name="shop", null=True)
