from django import template

register = template.Library()


@register.simple_tag
def PaymentCal(a, b, c):
    return int(a + (b * c))


@register.simple_tag
def AbsValue(a):
    return abs(a)
