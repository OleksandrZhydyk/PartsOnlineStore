from django.contrib import admin
from djongo.admin import ModelAdmin

from core.models import Shop


@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    list_display = ("address",)
    list_display_links = ("address",)
    search_fields = ("address", "part")
