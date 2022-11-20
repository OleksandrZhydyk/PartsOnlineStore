from django import template

register = template.Library()


@register.filter(name="discount_percent")
def discount_percent(discount):
    return round((1 - float(discount)) * 100)
