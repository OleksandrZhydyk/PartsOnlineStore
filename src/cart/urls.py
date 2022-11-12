from django.urls import path

from cart.views import add_to_cart, cart_view, delete_part_from_cart

urlpatterns = [
    path("<str:part_number>/", add_to_cart, name="add_to_cart"),
    path("", cart_view, name="cart_view"),
    path("<str:part_number>/delete", delete_part_from_cart, name="delete_part_from_cart")
]
