from django.forms import ModelForm

from orders.models import *
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ["number", "date","shop_address"]

    labels = {
        "client" : "client"
    }


class OrderLineForm(ModelForm):
    class Meta:
        model = OrderLine
        exclude = ["order", "product", "price", "warranty"]

        labels = {
            "quantity" : "number of items",
        }


class TestDriveForm(ModelForm):
    class Meta:
        model = TestDrive
        fields = ['product', 'date', 'location']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'product': 'Select a car',
            'date': 'Choose date and time',
            'location': 'Choose showroom location',
        }

