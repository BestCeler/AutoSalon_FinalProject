from django.contrib.admin import ModelAdmin
from django.contrib import admin

from cars_vw.models import Car, CarModel, CarColor

#class CardAdmin(ModelAdmin):
 #   @staticmethod

admin.site.register(CarModel)
admin.site.register(CarColor)
admin.site.register(Car)