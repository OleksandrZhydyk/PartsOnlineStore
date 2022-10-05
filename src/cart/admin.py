from django.contrib import admin

from cart.models import Cart, CartItem, OrdersHistory

admin.site.register([Cart, CartItem, OrdersHistory])
