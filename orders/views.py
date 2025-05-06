from django.db.models import Sum
from django.db.models.aggregates import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from cars_vw.models import Car
from orders.models import Order, OrderLine
from users.models import Address




class OrdersActions(View):
    def handle_order(self, request):
        return render(request, "home.html")
    def handle_orderline(self, request):
        return render(request, "home.html")
    def handle_order_finished(self, request):
        return render(request, "home.html")

    def setup(self, request, *args, **kwargs):
        super().setup(request,*args, **kwargs)
        self.order_ = request.session.get("order_")
        self.order_line_ = request.session.get("order_line_", [])
        if not Order.objects.filter(pk=self.order_).exists():
            self.order_ = None
            self.order_line_ = None


    def post(self,request):
        #(self.order_line_)
        if not self.order_:
            number_ = Order.objects.count() + 1
            client_ = request.user
            shop_address_ = request.POST.get("shop_address")
            get_shop_address_ = Address.objects.get(pk=shop_address_)

            self.order_ = Order.objects.create(number=number_, client=client_, shop_address=get_shop_address_)
            request.session["order_"] = self.order_.pk

            if self.order_:
                car_counter_ = 1

                get_order_ = self.order_
                product_ = request.POST.get(f"taken_car{car_counter_}")

                if self.order_line_:
                    get_data_ = OrderLine.objects.filter(order=self.order_)
                    for item in get_data_:
                        if product_ == item.product.pk:
                            car_counter_ += 1
                            product_ = request.POST.get(f"taken_car{car_counter_}")

                get_product_ = Car.objects.get(pk=product_)
                price_ = get_product_.price

                next_in_line_ = OrderLine.objects.create(order=get_order_, product=get_product_, price=price_)
                if self.order_line_:
                    line_ = request.session.get("line_")
                else:
                    line_ = []
                line_.append(next_in_line_.pk)
                request.session["order_line_"] = line_

            return self.handle_order(request)

        if self.order_:
            car_counter_ = 1

            get_order_ = Order.objects.get(pk=self.order_)
            product_ = request.POST.get(f"taken_car{car_counter_}")

            if self.order_line_:
                get_data_ = OrderLine.objects.filter(order=self.order_)
                for item in get_data_:
                    if int(product_) == int(item.product.pk):
                        car_counter_ += 1
                        product_ = request.POST.get(f"taken_car{car_counter_}")

            get_product_ = Car.objects.get(pk=product_)
            price_ = get_product_.price

            next_in_line_ = OrderLine.objects.create(order=get_order_, product=get_product_, price=price_)
            line_ = request.session.get("order_line_")
            line_.append(next_in_line_.pk)
            request.session["order_line_"] = line_

            return self.handle_orderline(request)



class OrderDetailView(DetailView):
    template_name = "order_processing.html"
    model = Order
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        count = []
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context["line"] = OrderLine.objects.filter(order=self.object)
        for query in context["line"]:
            context["cars"] = query.product
            print("my context:", context["cars"])
            count.append(Car.car_count(context["cars"]))
            context["cars_count"] = count
            print("car count:", context["cars_count"])

        #context["cars"] = Car.objects.filter(order)
        print(context["cars"])
        context["lines"] = OrderLine.objects.filter(order=self.object).values("product__model__name",
                                                                              "product__model",
                                                                              "product__transmission",
                                                                              "product__color",
                                                                              "product__price",).annotate(count = Count("id"),
                                                                                                  price = Sum("product__price"))
        #print(context["lines"])
        context["total_price"] = OrderLine.objects.filter(order=self.object).aggregate(s =  Sum("price"))["s"]
        #context["cars_count"] = Car.car_count(context["cars"])
        #print(context["cars_count"])

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

        context = []
        get_cars_ = Car.objects.filter(model=product_.model, color=product_.color, transmission=product_.transmission)
        print(f"cars: {get_cars_}")

        print(f"Product price: {product_.price}, Total: {total}")

        return JsonResponse({"total": total})
    except (Car.DoesNotExist, ValueError, TypeError) as e:
        print(f"error occurred {e}")
        return JsonResponse({"total": "Error"}, status=400)
