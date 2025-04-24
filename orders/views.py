from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from orders.models import Order
from users.models import Address

"""class MakeOrderView(View):
    model = Order

    order = None

    if not order:
        def post(self, request, *args, **kwargs):
            order_number_ = Order.objects.count() + 1
            client_ = request.user
            shop_address_ = request.POST.get("shop_address")
            order = Order.objects.create(number=order_number_, client=client_, shop_address=shop_address_)
            #reverse_lazy("car_filter")
            #render(request,"model.html")

            return order

    print(0)"""

"""order_ = None
order_line_ = None

def make_order(request):
    #global order_

    number_ = Order.objects.count() + 1
    client_ = request.user
    shop_address_ = request.POST.get("shop_address")
    my_shop_address_ = Address.objects.get(pk=shop_address_)
    #shop_address_ = Address.objects.create(shop_address_)
    print(my_shop_address_)

    order_ = Order.objects.create(number=number_, client=client_, shop_address=my_shop_address_)

    return render(request,"home.html")

print(order_)"""


class OrdersActions(View):
    order_ = None
    order_line_ = None

    def post(self,request):
        if not self.order_:
            number_ = Order.objects.count() + 1
            client_ = request.user
            shop_address_ = request.POST.get("shop_address")
            get_shop_address_ = Address.objects.get(pk=shop_address_)

            self.order_ = Order.objects.create(number=number_, client=client_, shop_address=get_shop_address_)
            return self.handle_order(request)

        if self.order_:
            get_order_ = self.order_
            product_ = request.POST.get("product")

    def handle_order(self, request):
        return render(request,"home.html")

    def handle_orderline(self, request):
        return render(request,"home.html")