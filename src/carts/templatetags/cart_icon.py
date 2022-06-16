from django import template
from carts.models import Order


register = template.Library()


@register.filter
def total_cart_items(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False).last()
        return order.get_total_quantity() if order else 0
    else:
        if 'device' in request.COOKIES.keys():
            order = Order.objects.filter(device=request.COOKIES['device'], ordered=False).last()
            return order.get_total_quantity() if order else 0
    return 0
