from django.db import models
from django import forms
from django_countries.fields import CountryField
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    current_address = models.BooleanField(default=False)

    def __str__(self):
        return f'Shipping address for {self.user.username}: {self.street} {self.street_number}, {self.city}'

    def get_absolute_url(self):
        return reverse('profile')


class ShippingAddressForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='Nombre', required=True)
    last_name = forms.CharField(max_length=100, label='Apellido', required=True)
    street = forms.CharField(max_length=150, label='Calle', required=True)
    street_number = forms.CharField(max_length=10, label='Número', required=True)
    city = forms.CharField(max_length=50, label='Ciudad', required=True)
    zip_code = forms.CharField(max_length=30, label='Código postal', required=True)
    phone = forms.CharField(max_length=30, label='Teléfono', required=True)
    save_address = forms.BooleanField(required=False, label='Guardar esta dirección de compra')


    class Meta:
        model = ShippingAddress
        fields = [
            'first_name',
            'last_name',
            'street',
            'street_number',
            'zip_code',
            'city',
            'phone'
        ]


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_id = models.CharField(max_length=60)
    amount = models.FloatField()
    issued_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} payment: {self.amount}'


class PromotionCode(models.Model):
    code = models.CharField(max_length=50)
    percentage_discount = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    def __str__(self):
        return self.code


class PromotionCodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].required = False

    class Meta:
        model = PromotionCode
        fields = ['code']
        labels = {
            'code': 'Código de descuento'
        }
