from django.forms import ModelForm, ValidationError
from cars_vw.models import Car, CarModel, Picture, CarColor

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

    # Add validation on price
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError("Price cannot be negative.")
        return price


class CarColorForm(ModelForm):
    class Meta:
        model = CarColor
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


    # Add a clean method for name autocorrection
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.title()
        return name

    # Add validation to the range field
    def clean_c_for(self):
        c_for = self.cleaned_data.get('c_for')
        if c_for is not None and c_for <= 0:
            raise ValidationError("The number of kilometers on a single charge cannot be < 0")
        return c_for

    # Add validation for the number of seats
    def clean_num_seats(self):
        num_seats = self.cleaned_data.get('num_seats')
        if num_seats is not None and num_seats <= 0:
            raise ValidationError("Number of seats must be greater than zero.")
        return num_seats


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = "__all__"
