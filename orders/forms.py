from django.forms import ModelForm

from orders.models import *
from django import forms

from django.utils import timezone


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ["number", "date","shop_address"]

    labels = {
        "client" : "client"
    }

    # checking if the client exists
    def clean_client(self):
        client = self.cleaned_data.get('client')
        if client is None:
            raise forms.ValidationError("Client must be selected.")
        return client


class OrderLineForm(ModelForm):
    class Meta:
        model = OrderLine
        exclude = ["order", "product", "price", "warranty"]

        labels = {
            "quantity" : "number of items",
        }

        # Check that quantity is positive (greater than 0).
        def clean_quantity(self):
            quantity = self.cleaned_data.get('quantity')
            if quantity is None or quantity <= 0:
                raise forms.ValidationError("Quantity must be greater than zero.")
            return quantity


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


        # Check if there is a date in the future
        def clean_date(self):
            date = self.cleaned_data.get('date')
            if date and date <= timezone.now():
                raise forms.ValidationError("Date and time must be in the future.")
            return date




