from django import template
from products.models import Category

register = template.Library()


@register.filter
def total_categories(arg=None):
    return Category.objects.all()
