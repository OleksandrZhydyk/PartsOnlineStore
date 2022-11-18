from django.contrib import admin
from djongo.admin import ModelAdmin

from cart.models import Cart, CartItem


class CartItemInline(admin.StackedInline):
    model = CartItem


@admin.register(Cart)
class Cart(ModelAdmin):
    inlines = [CartItemInline]
    date_hierarchy = 'creation_date'
    ordering = ('creation_date',)
    list_display = ('creation_date', 'order_id', 'phone_number', 'city', 'total_amount')
    list_display_links = ('order_id',)
    search_fields = ('order_id', 'city', 'phone_number')


@admin.register(CartItem)
class CartItem(ModelAdmin):
    list_display = ["pk", "part_number", "part_name", "price", "discount", "cart"]
    ordering = ('cart',)
    list_display_links = ('pk', "part_number")
    search_fields = ('part_number', 'part_name', 'cart')

