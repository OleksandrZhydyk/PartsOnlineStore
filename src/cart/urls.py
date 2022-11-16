from django.urls import path

from cart.views import add_to_cart, cart_view, delete_part_from_cart, make_order, get_orders_history

urlpatterns = [
    path("add_to_cart/<str:part_number>/", add_to_cart, name="add_to_cart"),
    path("", cart_view, name="cart_view"),
    path("<str:part_number>/delete", delete_part_from_cart, name="delete_part_from_cart"),
    path("make_order/", make_order, name="make_order"),
    path("orders_history/<uuid:pk>/", get_orders_history, name="orders_history"),
    # path("make_order/incorrect_quantity/<str:part_number>/", incorrect_quantity, name="incorrect_quantity"),
]
