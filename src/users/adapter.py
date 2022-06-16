from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from carts.models import Order


class CustomAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            cart = Order.objects.filter(device=request.COOKIES['device'], ordered=False).last()
            if cart:
                cart.user = request.user
                items = cart.get_all_items()
                for item in items:
                    item.user = request.user
                    item.save()
                cart.save()
        return reverse('products:home-page')