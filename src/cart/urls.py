from django.urls import path

from cart.views import (add_to_cart, delete_part_from_cart, get_ordered_cart,
                        get_orders_history, make_order, view_cart)

urlpatterns = [
    path("add_to_cart/<str:part_number>/", add_to_cart, name="add_to_cart"),
    path("", view_cart, name="view_cart"),
    path("<str:part_number>/delete", delete_part_from_cart, name="delete_part_from_cart"),
    path("make_order/", make_order, name="make_order"),
    path("orders_history/<uuid:pk>/", get_orders_history, name="orders_history"),
    path("ordered_cart/<int:cart_pk>/", get_ordered_cart, name="get_ordered_cart"),
]
