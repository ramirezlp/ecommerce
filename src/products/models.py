from django.db import models
from django.shortcuts import reverse
from PIL import Image


# Create your models here.

class BodyPart(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    subname = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', null=True)
    

    def __str__(self):
        return self.name



class Size(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=4)
    body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    IMG_DIMENSION = 540

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='products/%Y/%m/%d/')
    important = models.BooleanField(default=False)
    body_part = models.ForeignKey(BodyPart, null=True, blank=True, on_delete=models.SET_NULL)
    sizes = models.ManyToManyField(Size, through='ProductSize')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name

    def save(self):
        super().save()

        with Image.open(self.thumbnail.path) as img:
            if img.height > self.IMG_DIMENSION or img.width > self.IMG_DIMENSION:
                img.thumbnail((self.IMG_DIMENSION, self.IMG_DIMENSION))
                img.save(self.thumbnail.path)

    def get_product_url(self):
        return reverse("products:product-detail", kwargs={
            'pk': self.pk
        })

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + ' - ' + self.product.name + ' - ' + self.size.size