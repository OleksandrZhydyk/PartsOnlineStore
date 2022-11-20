from django.contrib import admin
from djongo.admin import ModelAdmin

from catalogue.models import MachineModel, Part


@admin.register(Part)
class PartAdmin(ModelAdmin):
    date_hierarchy = "date_created"
    ordering = ("date_created",)
    list_display = ("part_number", "part_name", "price", "discount_price", "stock_quantity", "machine_system")
    list_display_links = ("part_number",)
    search_fields = ("part_number", "part_name", "discount_price", "machine_system")


@admin.register(MachineModel)
class MachineModelAdmin(ModelAdmin):
    list_display = ("model", "machine_type")
    list_display_links = ("model",)
    search_fields = ("model", "machine_type")
