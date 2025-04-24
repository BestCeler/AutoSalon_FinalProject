from django.forms import ModelForm, DateField

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

class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = "__all__"