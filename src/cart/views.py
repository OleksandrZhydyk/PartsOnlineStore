from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cart.models import Cart, CartItem
from catalogue.models import Part


def add_to_cart(request, **kwargs):
    cart = request.session.get("cart")
    part_number = kwargs.get("part_number")
    part = Part.objects.get(part_number=part_number)
    quantity = request.GET.get("quantity")
    # check if cart key exists in session
    if cart:
        print(cart)
        part_data = cart.get(str(part_number))
        print(part_data)
        # if duplicate of part added, summarize q-ty
        if part_data:
            quantity_before = request.session['cart'][part_number]['quantity']
            request.session['cart'][part_number]['quantity'] = str(int(quantity) + int(quantity_before))
            request.session.modified = True
        else:
            request.session['cart'][part_number] = {'quantity': quantity, 'price': part.price}
            request.session.modified = True
    # initialize cart dict in session
    else:
        request.session['cart'] = {}
        request.session['cart'][part_number] = {'quantity': quantity, 'price': part.price}
        request.session.modified = True

    return HttpResponseRedirect(reverse("parts_view"))


def get_total_cost(cart_data):
    return round(sum(int(value['quantity'])*value['price'] for value in cart_data.values()), 2)


def cart_view(request):
    cart_data = request.session.get('cart')
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
            context={"title": "Cart", "parts": parts,
                     "cart_data": cart_data,
                     "total_cart_cost": total_cart_cost},
            )


def delete_part_from_cart(request, **kwargs):
    cart_data = request.session.get('cart')
    part_number = kwargs.get("part_number")
    del cart_data[part_number]
    request.session.modified = True
    return HttpResponseRedirect(reverse("cart_view"))

# @login_required
# def make_order(request):
#     cart = Cart.objects.create()


# def cart_view(request):
#     cart_id = request.session.get("cart")
#     cart = Cart.objects.get(pk=cart_id)
#     return render(
#         request,
#         template_name="cart/cart.html",
#         context={"title": "Cart", "cart": cart},
#     )
