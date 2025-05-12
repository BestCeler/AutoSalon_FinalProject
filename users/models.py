from django.db.models import Model, CharField, ForeignKey, IntegerField, OneToOneField
from django.db import models
from django.contrib.auth.models import User


# creates an address to be used either in users or elsewhere
class Address(Model):
    city = CharField(max_length=100, null=False, blank=False)
    postcode = CharField(max_length=30, null=False, blank=False)
    street = CharField(max_length=100, null=False, blank=False)
    country = CharField(max_length=100, null=False, blank=False)
    state = CharField(max_length=100, null=True, blank=True) # will be used if user is from USA




class Profile(Model):
    user = OneToOneField(User, on_delete=models.CASCADE) # Uses OTOF to get fill the variable with created user
    address = ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    phone_num = IntegerField(null=False, blank=False)