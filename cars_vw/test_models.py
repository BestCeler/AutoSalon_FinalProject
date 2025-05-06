from django.test import TestCase
from cars_vw.models import CarModel, CarColor, Car
from datetime import date

class CarTestCase(TestCase):

    def setUp(self):
        self.model = CarModel.objects.create(
            name="Model S",
            c_for=600,
            description="Luxury electric sedan",
            num_seats=5
        )

        self.color = CarColor.objects.create(name="Red")

        self.car = Car.objects.create(
            model=self.model,
            transmission=True,
            color=self.color,
            price=90000,
            designation=True,
            test_drive=True,
            cid="TESLA001",
            location="Prague"
        )

    def test_car_model_str(self):
        self.assertEqual(str(self.model), "car model Model S with 5 seats and 600km of range")

    def test_car_color_str(self):
        self.assertEqual(str(self.color), "color: Red")

    def test_car_str(self):
        self.assertIn("this car is of model", str(self.car))

    def test_car_foreign_keys(self):
        self.assertEqual(self.car.model.name, "Model S")
        self.assertEqual(self.car.color.name, "Red")

    def test_car_defaults(self):
        self.assertEqual(self.car.transmission, True)
        self.assertEqual(self.car.designation, True)
