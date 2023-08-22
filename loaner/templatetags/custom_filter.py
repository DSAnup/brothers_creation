from django import template

register = template.Library()


@register.simple_tag
def calculateInterest(a, b):
    return int((a * b) / 100)
