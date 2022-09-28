from django.contrib.auth import get_user_model
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    payment_type = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    ordered = models.BooleanField(default=False)

