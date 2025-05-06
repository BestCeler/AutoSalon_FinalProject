import datetime

from django.test import TestCase

from cars_vw.forms import *
from cars_vw.models import *


class CarFormTests(TestCase):

    def setUp(self):
        self.model = CarModel.objects.create(name="model x", c_for=550,
                                             description="electric suv", num_seats=5)
        self.color = CarColor.objects.create(name="black")

    def test_valid_car_form(self):
        form_data = {
            'model': self.model.id,
            'transmission': True,
            'color': self.color.id,
            'price': 85000,
            'designation': True,
            'test_drive': False,
            'cid': 'TESLA123',
            'location': 'Prague'
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_price(self):
        form_data = {
            'model': self.model.id,
            'transmission': False,
            'color': self.color.id,
            'price': -100,
            'designation': False,
            'test_drive': True,
            'cid': 'TESLA999',
            'location': 'Brno'
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

class CarModelFormTests(TestCase):


    def test_valid_model_form(self):
        form_data = {
            'name': 'cybertruck',
            'c_for': 800,
            'description': ' futuristic pickup ',
            'num_seats': 4
        }
        form = CarModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_name_title(self):
        form_data = {
            'name': 'roadster x',
            'c_for': 1000,
            'description': 'sport electric car',
            'num_seats': 2
        }
        form = CarModelForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['name'], 'Roadster X')

    def test_negative_range_invalid(self):
        form_data = {
            'name': 'semi',
            'c_for': -200,
            'description': 'truck',
            'num_seats': 2
        }
        form = CarModelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('c_for', form.errors)

    def test_negative_seats_invalid(self):
        form_data = {
            'name': 'mini',
            'c_for': 250,
            'description': 'tiny model',
            'num_seats': 0
        }
        form = CarModelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('num_seats', form.errors)
