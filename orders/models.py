from django.db import models
from django.db.models import Model, IntegerField, DateField, ForeignKey, DateTimeField
from users.models import User, Address
from cars_vw.models import Car


# Creates an order for a car
class Order(Model):
    number = IntegerField(null=False, blank=False) # number of the order
    date = DateField(auto_now_add=True ,null=False, blank=False) # date of order creation
    client = ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='orders') # takes from the db users
    shop_address = ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, related_name='orders') # Address can be saved in the address db

# Creates a line from orders, e.g allows us to pair multiple articles to a single order
class OrderLine(Model):
    order = ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lines')
    product = ForeignKey(Car, null=False, blank=False, on_delete=models.CASCADE, related_name='lines')
    quantity = IntegerField(null=False, blank=False)
    price = IntegerField(null=False, blank=False)
    warranty = IntegerField(null=False, blank=False, default=2) # how long is the warranty


class TestDrive(Model):
    client = ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='test_drives')
    product = ForeignKey(Car, null=False, blank=False, on_delete=models.CASCADE, related_name='test_drives')
    date = DateTimeField(auto_now_add=False, null=False, blank=False)
    location = ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, related_name='test_drives')


class Rents(Model):
    client = ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='rents')
    product = ForeignKey(Car, null=False, blank=False, on_delete=models.CASCADE, related_name='rents')
    date_from = DateTimeField(auto_now_add=False, null=False, blank=False)
    date_to = DateTimeField(auto_now_add=False, null=False, blank=False)
    location = ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, related_name='rents')

