from django.contrib import admin

from orders.models import Order, OrderLine, TestDrive, Rents

admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(TestDrive)
admin.site.register(Rents)