from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from cars_vw.models import Car
from orders.models import Order, OrderLine
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
    def setup(self, request, *args, **kwargs):
        super().setup(request,*args, **kwargs)
        self.order_ = request.session.get("order_")
        self.order_line_ = request.session.get("order_line_")

    def post(self,request):
        #(self.order_line_)
        if not self.order_:
            number_ = Order.objects.count() + 1
            client_ = request.user
            shop_address_ = request.POST.get("shop_address")
            get_shop_address_ = Address.objects.get(pk=shop_address_)

            self.order_ = Order.objects.create(number=number_, client=client_, shop_address=get_shop_address_)
            request.session["order_"] = self.order_.pk
            #print(self.order_)

            if self.order_:
                get_order_ = self.order_
                product_ = request.POST.get("taken_car")
                #print(product_)
                get_product_ = Car.objects.get(pk=product_)
                print(get_product_)
                price_ = get_product_.price

                next_in_line_ = OrderLine.objects.create(order=get_order_, product=get_product_, price=price_)
                request.session["order_line_"] = next_in_line_.pk

            return self.handle_order(request)

        if self.order_:
            get_order_ = Order.objects.get(pk=self.order_)
            product_ = request.POST.get("taken_car")
            get_product_ = Car.objects.get(pk=product_)
            print(get_product_)
            price_ = get_product_.price

            next_in_line_ = OrderLine.objects.create(order=get_order_, product=get_product_, price=price_)
            last_in_line_ = request.session.get("order_line_")
            request.session["order_line_"] += next_in_line_.pk

            return self.handle_orderline(request)

        def handle_order(self, request):
            return render(request, "home.html")

        def handle_orderline(self, request):
            return render(request, "home.html")

        def handle_order_finished(self, request):
            return render(request, "home.html")


class OrderDetailView(DetailView):
    template_name = "order_processing.html"
    model = Order
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context["line"] = OrderLine.objects.filter(order=self.object)
        context["total_price"] = OrderLine.objects.filter(order=self.object).aggregate(s =  Sum("price"))["s"]

        return context


def calculate_price(request, pk):
    try:
        quantity = int(request.GET.get("quantity", 1))
    except ValueError:
        quantity = 1

    try:
        product_ = Car.objects.get(pk=pk)
        print(product_)
        car_price_ = product_.price
        total = int(car_price_ * quantity)

        print(f"Product price: {product_.price}, Total: {total}")

        return JsonResponse({"total": total})
    except (Car.DoesNotExist, ValueError, TypeError) as e:
        print(f"error occurred {e}")
        return JsonResponse({"total": "Error"}, status=400)
