from django.db.models import Sum
from django.db.models.aggregates import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from cars_vw.models import Car
from orders.forms import TestDriveForm, RentForm
from orders.models import Order, OrderLine, TestDrive, Rents
from users.models import Address



class OrdersActions(View):
    def handle_order(self, request):
        return render(request, "home.html")
    def handle_orderline(self, request):
        return render(request, "home.html")

    def setup(self, request, *args, **kwargs):
        super().setup(request,*args, **kwargs)
        self.order_ = request.session.get("order_")
        self.order_line_ = request.session.get("order_line_", [])
        if not Order.objects.filter(pk=self.order_).exists():
            self.order_ = None
            self.order_line_ = None

    def post(self,request):
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




class FinishOrderView(DetailView):
    model = Order
    template_name = "finish_order.html"
    context_object_name = "finish"

    def get_context_data(self, **kwargs):
        context = super(FinishOrderView, self).get_context_data(**kwargs)
        context["order_line"] = OrderLine.objects.filter(order=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        lines = OrderLine.objects.filter(order=self.object)
        line_aggregate = OrderLine.objects.filter(order=self.object).values(
                                                                     "product__model__name",
                                                                     "product__color",
                                                                     "product__transmission",
                                                                     "product__price").annotate(count = Count("id"))

        for car in line_aggregate:
            print("car id", car["count"])
        counter = 1
        while request.POST.get(f"quantity_{counter}"):
            quantity = int(request.POST.get(f"quantity_{counter}"))
            while quantity < line_aggregate[counter-1]["count"]:
                OrderLine.objects.filter(order=self.object,
                                         product__model__name=line_aggregate[counter-1]["product__model__name"],
                                         product__color=line_aggregate[counter-1]["product__color"],
                                         product__transmission=line_aggregate[counter-1]["product__transmission"],
                                         product__price=line_aggregate[counter-1]["product__price"]).first().delete()
                quantity += 1
            while quantity > line_aggregate[counter-1]["count"]:
                new_car = Car.objects.filter(model__name=line_aggregate[counter-1]["product__model__name"],
                                             transmission=line_aggregate[counter-1]["product__transmission"],
                                             color=line_aggregate[counter-1]["product__color"],
                                             price=line_aggregate[counter-1]["product__price"])
                for car in lines:
                    if car.product in new_car:
                        new_car = new_car.exclude(id=car.product.id)
                new_car = new_car.first()
                OrderLine.objects.create(order=self.object,
                                         product=new_car,
                                         price=new_car.price,)
                quantity -= 1

            counter += 1
        request.session["order_"] = None
        return render(request, self.template_name)




class OrderDetailView(DetailView):
    template_name = "order_processing.html"
    model = Order
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context["lines"] = OrderLine.objects.filter(order=self.object).values("product__model__name",
                                                                              "product__model",
                                                                              "product__transmission",
                                                                              "product__color",
                                                                              "product__price",).annotate(count = Count("id"),
                                                                                                  price = Sum("product__price"))
        for car in context["lines"]:
            car_ = Car.objects.filter(model=car["product__model"],
                                      transmission=car["product__transmission"],
                                      color=car["product__color"]).first()
            car["max_count"] = car_.car_count
        context["total_price"] = OrderLine.objects.filter(order=self.object).aggregate(s =  Sum("price"))["s"]
        return context


def calculate_price(request, pk): # calcualtes price from html and javascript
    # attempts to get quantity, default is 1
    try:
        quantity = int(request.GET.get("quantity", 1))
    except ValueError:
        quantity = 1

    try: # gets needed information from the site
        product_ = Car.objects.get(pk=pk)
        car_price_ = product_.price
        total = int(car_price_ * quantity)

        get_cars_ = Car.objects.filter(model=product_.model, color=product_.color, transmission=product_.transmission)

        print(f"cars: {get_cars_}")
        print(f"Product price: {product_.price}, Total: {total}")

        return JsonResponse({"total": total}) # respond to javascript
    except (Car.DoesNotExist, ValueError, TypeError) as e:
        print(f"error occurred {e}")
        return JsonResponse({"total": "Error"}, status=400)

@login_required
def book_rent(request):
    if request.method == "POST":
        form = RentForm(request.POST)
        if form.is_valid():
            rent = form.save(commit=False)
            rent.client = request.user
            rent.save()
            return redirect('rent_detail', pk=rent.pk)
    else:
        form = RentForm()
    return render(request, "rent_form.html", {"form": form})

# shows the rental page for a specific car
class RentDetailView(DetailView):
    model = Rents
    template_name = "rent_detail.html"
    context_object_name = "rent"

class TestDriveDetailView(DetailView):
    model = TestDrive
    template_name = "test_drive.html"
    context_object_name = "testdrive"

# function for creating (booking) a test drive
@login_required
def book_test_drive(request):
    if request.method == "POST":
        form = TestDriveForm(request.POST)
        if form.is_valid():
            test_drive = form.save(commit=False)
            test_drive.client = request.user
            test_drive.save()
            return redirect("testdrive_detail", pk=test_drive.pk)
    else:
        form = TestDriveForm()

    return render(request, "test_drive.html", {"form": form})