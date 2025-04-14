import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateField

from cars_vw.models import Car, CarModel


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

    labels = {
        "model" : "car model",
        "transmission" : "transmission",
        "color" : "color",
        "established" : "date of shop attainment",
        "price" : "price",
        "designation" : "designation",
        "test_drive" : "test drive",
        "cid" : "car identification number",
        "location" : "location"
    }

    help_texts = {
        "transmission" : "manual/automatic",
        "designation" : "rent/sale",
        "test_drive" : "y/n"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_price(self):
        initial = int(self.cleaned_data['price'])
        if initial is not None and initial <= 0:
            raise ValidationError("Price must be a positive number.")
        return initial



class CarColorForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"


class CarModelForm(ModelForm):
    class Meta:
        model = CarModel
        fields = "__all__"

    labels = {
        "name" : "model name",
        "c_for" : "field of range",
        "num_seats" : "number of seats"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        if initial:
            return initial.title()
        return initial

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean_c_for(self):
        initial = int(self.cleaned_data['c_for'])
        if initial is not None and initial <= 0:
            raise ValidationError("Must be a positive number.")
        return initial

    def clean_num_seats(self):
        initial = int(self.cleaned_data['num_seats'])
        if initial is not None and initial <= 0:
            raise ValidationError("Must be a positive number.")
        return initial

