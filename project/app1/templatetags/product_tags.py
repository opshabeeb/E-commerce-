from django import template
import math
register = template.Library()

@register.simple_tag
def cal_sellprice(price,discount):
    if discount is None or discount is 0:
        return price
    sellprice=(price)
    sellprice=price -(price * discount/100)
    return math.floor(sellprice)
@register.filter
def mul(value, arg):
    return value * arg