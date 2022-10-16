# Generated by Django 4.1.1 on 2022-10-16 06:33

import catalogue.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Part",
            fields=[
                (
                    "part_number",
                    models.CharField(
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                        validators=[catalogue.validators.part_number_validator],
                    ),
                ),
                (
                    "part_name",
                    models.CharField(
                        max_length=125, null=True, verbose_name="Part name"
                    ),
                ),
                (
                    "price",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=0.01,
                                message="Price has to be greater then 0.01.",
                            )
                        ],
                        verbose_name="Price",
                    ),
                ),
                (
                    "discount_price",
                    models.FloatField(blank=True, null=True, verbose_name="Discount"),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Part adding date"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="profiles_avatars/empty_avatar.png",
                        null=True,
                        upload_to="profiles_avatars/%Y/%m/%d/",
                        verbose_name="Image",
                    ),
                ),
                (
                    "remark",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Remark"
                    ),
                ),
                (
                    "stock_quantity",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MachineModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model", models.CharField(max_length=15, verbose_name="Model")),
                (
                    "machine_type",
                    models.IntegerField(
                        choices=[
                            (1, "Tractor"),
                            (2, "Combine"),
                            (3, "Self-propelled sprayer"),
                            (4, "Self-propelled forage combine"),
                            (5, "Loader"),
                        ],
                        default=1,
                        verbose_name="Machine type",
                    ),
                ),
                (
                    "part",
                    models.ManyToManyField(
                        related_name="machine_model", to="catalogue.part"
                    ),
                ),
            ],
        ),
    ]
