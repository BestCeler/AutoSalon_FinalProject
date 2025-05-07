from django.forms import ModelForm

from orders.models import *
from django import forms

from django.utils import timezone

from django.core.exceptions import ValidationError


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


class TestDriveForm(ModelForm): # form for booking a drive
    class Meta:
        model = TestDrive
        fields = ['product', 'date', 'location']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}), # widget for better user experience
        }
        labels = {
            'product': 'Select a car',
            'date': 'Choose date and time',
            'location': 'Choose showroom location',
        }


        # Check if there is a date in the future
        def clean_date(self):
            date = self.cleaned_data.get('date')
            if date and date <= timezone.now(): # checks validity
                raise forms.ValidationError("Date and time must be in the future.")
            return date


class RentForm(ModelForm): # form for booking rents
    class Meta:
        model = Rents
        fields = ['product', 'date_from', 'date_to', 'location']

        widgets = {
            'date_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        labels = {
            'product': 'Select a car',
            'date_from': 'Start date and time',
            'date_to': 'End date and time',
            'location': 'Pickup location',
        }

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        product = cleaned_data.get('product')

        if date_from and date_to:
            if date_to <= date_from:
                raise ValidationError('End date must be after start date.')

            # Lease overlap check
            overlapping_rents = Rents.objects.filter(
                product=product,
                date_from__lt=date_to,
                date_to__gt=date_from
            )
            if self.instance.pk:
                overlapping_rents = overlapping_rents.exclude(pk=self.instance.pk)

            if overlapping_rents.exists():
                raise ValidationError('This car is already rented during the selected period.')

        return cleaned_data
