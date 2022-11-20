from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.models import Profile
from cart.forms import CartForm
from cart.models import Cart, CartItem
from cart.services.order_id import get_order_id
from catalogue.models import Part


def add_to_cart(request, **kwargs):
    cart = request.session.get("cart")
    part_number = kwargs.get("part_number")
    part = Part.objects.get(part_number=part_number)
    quantity = request.GET.get("quantity")
    # check if cart key exists in session
    if cart:
        part_data = cart.get(str(part_number))
        # if duplicate of part added, summarize q-ty
        if part_data:
            quantity_before = request.session["cart"][part_number]["quantity"]
            request.session["cart"][part_number]["quantity"] = str(int(quantity) + int(quantity_before))
            request.session.modified = True
        # if there is no part, add to session cart dict
        else:
            request.session["cart"][part_number] = {
                "quantity": quantity,
                "price": part.price,
                "part_name": part.part_name,
                "discount": part.discount_price,
            }
            request.session.modified = True
    # initialize cart dict in session
    else:
        request.session["cart"] = {}
        request.session["cart"][part_number] = {
            "quantity": quantity,
            "price": part.price,
            "part_name": part.part_name,
            "discount": part.discount_price,
        }
        request.session.modified = True

    return HttpResponseRedirect(reverse("parts_view"))


def get_total_cost(cart_data):
    return round(sum(int(value["quantity"]) * value["price"] * value["discount"] for value in cart_data.values()), 2)


def view_cart(request):
    cart_data = request.session.get("cart")
    if cart_data:
        part_numbers = [part_number for part_number in cart_data]
        parts = Part.objects.filter(part_number__in=part_numbers)
        total_cart_cost = get_total_cost(cart_data)
    else:
        parts = []
        total_cart_cost = 0

    return render(
        request,
        template_name="cart/cart.html",
        context={"title": "Cart", "parts": parts, "cart_data": cart_data, "total_cart_cost": total_cart_cost},
    )


def delete_part_from_cart(request, **kwargs):
    cart_data = request.session.get("cart")
    part_number = kwargs.get("part_number")
    del cart_data[part_number]
    request.session.modified = True
    return HttpResponseRedirect(reverse("view_cart"))


@login_required
def make_order(request):
    cart_data = request.session.get("cart")
    if request.GET and cart_data:
        for part_number, quantity in request.GET.items():
            cart_data[part_number]["quantity"] = quantity[0]
        request.session["cart"] = cart_data
    if request.method == "POST":
        form = CartForm(request.POST)
        if form.is_valid():
            # create cart with cart items
            cart = form.save(commit=False)
            cart.user = request.user
            cart.total_amount = get_total_cost(cart_data)
            cart.save()
            bulk_part_list = []
            for part_number, value in cart_data.items():
                part = Part.objects.get(part_number=part_number)
                quantity = value.get("quantity")
                # check part availability on the stock
                if part.stock_quantity < int(quantity):
                    return render(
                        request, template_name="cart/order_confirmation.html", context={"order_id": cart.order_id}
                    )

                bulk_part_list.append(
                    CartItem(
                        part=part,
                        cart=cart,
                        quantity=quantity,
                        part_number=part.part_number,
                        part_name=part.part_name,
                        price=part.price,
                        discount=part.discount_price,
                    )
                )
            CartItem.objects.bulk_create(bulk_part_list)
            # clean session cart dict
            del request.session["cart"]
            request.session.modified = True
            return render(
                request,
                template_name="cart/order_confirmation.html",
                context={"title": "Ordered", "order_id": cart.order_id},
            )
    else:
        # final confirm form before order
        form = CartForm(initial={"order_id": get_order_id(request.user.pk)})
        profile = Profile.objects.get(user=request.user)
    total_cart_cost = get_total_cost(cart_data)
    return render(
        request,
        template_name="cart/make_order.html",
        context={"form": form, "total_cart_cost": total_cart_cost, "cart_data": cart_data, "profile": profile},
    )


@login_required
def get_orders_history(request, **kwargs):
    carts = Cart.objects.filter(user=request.user).order_by("-creation_date")
    return render(
        request,
        template_name="cart/orders_history.html",
        context={"title": "Orders history", "carts": carts},
    )


@login_required
def get_ordered_cart(request, **kwargs):
    cart = Cart.objects.get(pk=kwargs.get("cart_pk"))
    cart_items = CartItem.objects.filter(cart_id=kwargs.get("cart_pk"))
    return render(
        request,
        template_name="cart/ordered_cart.html",
        context={"title": "Ordered cart", "cart": cart, "cart_items": cart_items},
    )
