from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

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
            quantity_before = request.session['cart'][part_number]['quantity']
            request.session['cart'][part_number]['quantity'] = str(int(quantity) + int(quantity_before))
            request.session.modified = True
        else:
            request.session['cart'][part_number] = {'quantity': quantity,
                                                    'price': part.price,
                                                    'part_name': part.part_name}
            request.session.modified = True
    # initialize cart dict in session
    else:
        request.session['cart'] = {}
        request.session['cart'][part_number] = {'quantity': quantity,
                                                'price': part.price,
                                                'part_name': part.part_name}
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

#
# def fill_cart(cart_data, cart):
#     bulk_part_list = []
#     for part_number, value in cart_data.items():
#         part = Part.objects.get(part_number=part_number)
#         quantity = value.get('quantity')
#         if part.stock_quantity < int(quantity):
#             print("here")
#             return render(request, template_name="cart/ordered_quantity_exceed.html",
#                           context={"part": part})
#
#         bulk_part_list.append(
#             CartItem(part=part, cart=cart, quantity=quantity)
#         )
#     CartItem.objects.bulk_create(bulk_part_list)
#     return render(request, template_name="cart/orders_history.html",
#                           context={"cart": cart})


@login_required
def make_order(request):
    cart_data = request.session.get('cart')
    if request.method == "POST":
        form = CartForm(request.POST)
        if form.is_valid():
            # create cart with cart items
            cart = form.save(commit=False)
            cart.user = request.user
            cart.save()
            bulk_part_list = []
            for part_number, value in cart_data.items():
                part = Part.objects.get(part_number=part_number)
                quantity = value.get('quantity')
                # check part availability on the stock
                if part.stock_quantity < int(quantity):
                    return render(request, template_name="cart/order_confirmation.html",
                                  context={"order_id": cart.order_id})

                bulk_part_list.append(
                    CartItem(part=part, cart=cart, quantity=quantity)
                )
            CartItem.objects.bulk_create(bulk_part_list)
            # clean session cart dict
            del request.session['cart']
            request.session.modified = True
            return render(request, template_name="cart/order_confirmation.html",
                          context={"title": "Ordered", "order_id": cart.order_id})
    else:
        # final confirm form before order
        form = CartForm(initial={'order_id': get_order_id(request.user.pk)})
        cart_data = request.session.get('cart')
    total_cart_cost = get_total_cost(cart_data)
    return render(request, template_name="cart/make_order.html",
                  context={"form": form,
                           "total_cart_cost": total_cart_cost,
                           "cart_data": cart_data,
                           }
                  )


def get_orders_history(request, **kwargs):
    carts = Cart.objects.filter(user=request.user)
    return render(
            request,
            template_name="cart/orders_history.html",
            context={"title": "Orders history", "carts": carts},
            )
