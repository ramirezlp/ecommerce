from django.contrib import admin

from .models import Category
from .models import Product
from .models import Size
from .models import BodyPart
from .models import ProductSize

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(BodyPart)
admin.site.register(ProductSize)