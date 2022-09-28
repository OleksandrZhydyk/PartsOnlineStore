from django.db import models


class Shop(models.Model):
    address = models.CharField(max_length=255)
