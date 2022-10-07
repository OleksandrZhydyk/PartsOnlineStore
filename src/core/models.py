from django.db import models

from catalogue.models import Part


class Shop(models.Model):
    address = models.CharField(max_length=255)
    part = models.ForeignKey(to=Part, related_name="shop", on_delete=models.CASCADE, null=True)
