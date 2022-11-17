from django import template

register = template.Library()


@register.filter(name="multiply")
def multiply(value):
    return round(int(value['quantity']) * value['price'] * value['discount'], 2)