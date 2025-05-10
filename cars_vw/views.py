from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cars_vw.forms import CarModelForm
from cars_vw.models import Car, CarModel, CarColor, Picture
from users.models import Address

from dotenv import load_dotenv
load_dotenv()

import os
import requests
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


class ModelsListView(ListView):
    template_name = 'models.html'
    model = CarModel
    context_object_name = 'models'



class CarToModelDetailView(DetailView):
    template_name = 'model.html'
    model = CarModel
    context_object_name = 'model'

    def get_context_data(self, **kwargs): # context for displaying correct information
        context = super().get_context_data(**kwargs)
        context["colors"] = CarColor.objects.filter(cars__model=self.object).distinct()
        get_address_ = Address.objects.filter(cars__model=self.object).first()
        context["address"] = get_address_
        if context["colors"]:
            default_color_ = context['colors'][0]
            context["cars"] = Car.objects.filter(model=self.object, color=default_color_)
        else:
            context["cars"] = Car.objects.filter(model=self.object)

        context["selected_car"] = context["cars"].first()

        return context



class CarFilterView(DetailView):
    def post(self, request, *args, **kwargs):
        color_ = self.request.POST.get("color")
        model_ = self.request.POST.get("model")
        transmission_ = self.request.POST.get("transmission")
        get_model = CarModel.objects.get(pk=model_)
        context = {}
        context["model"] = get_model
        context["colors"] = CarColor.objects.filter(cars__model= get_model).distinct()
        context["cars"] = Car.objects.filter(model=model_, color=color_, transmission=transmission_)
        if context["cars"]:
            cars = context["cars"][0]
        else:
            cars = None
        context["address"] = Address.objects.filter(cars=cars).first()

        return render(request, "model.html", context)



class ModelCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CarModelForm      # TODO add to form.py
    success_url = reverse_lazy('models')
    permission_required = 'cars_vw.add_car'

    def form_invalid(self, form):
        print("Form 'CreatorModelForm' is not valid.")
        return super().form_invalid(form)


class ModelUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CarModelForm
    model = CarModel
    success_url = reverse_lazy('models')
    permission_required = 'cars_vw.change_car'

    def form_invalid(self, form):
        print("Form 'CreatorModelForm' is not valid.")
        return super().form_invalid(form)


class ModelDeleteView(#StaffRequiredMixin,
        PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = CarModel
    success_url = reverse_lazy('models')
    permission_required = 'cars_vw.delete_car'


def search(request):
    if request.method == 'POST':
        search_string = request.POST.get('search').strip()
        if search_string:
            name = CarModel.objects.filter(name__contains=search_string)
            c_for = CarModel.objects.filter(c_for__contains=search_string)
            description = CarModel.objects.filter(description__contains=search_string)
            num_seats = CarModel.objects.filter(num_seats__contains=search_string)

            context = {'search': search_string,
                       'name': name,
                       'c_for': c_for,
                       'description': description,
                       'num_seats': num_seats}

            return render(request, 'search.html', context)
    return render(request, 'home.html')



# Load your API key from environment
API_KEY = os.getenv("EXCHANGERATESAPI_KEY")
# print(f"Exchange API KEY: '{API_KEY}'")

def convert_eur_to_czk(request):
    if not API_KEY:
        return JsonResponse({"error": "API key missing"}, status=500)

    amount = request.GET.get("amount")  # Let's try to take the number of euros
    url = f"http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&base=EUR&symbols=CZK"
    headers = {
        "apikey": API_KEY,
    }
    print(f"url: {url}")
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        print(f"respons: {response}")
        print(f"data: {data}")
        if response.status_code != 200:
            return JsonResponse({
                "error": "Failed to retrieve exchange rates",
                "details": data
            }, status=response.status_code)

        rate = data["rates"].get("CZK")
        if not rate:
            return JsonResponse({"error": "Rate not found"}, status=500)

        if amount:
            try:
                amount = float(amount)
                if amount < 0:
                    return JsonResponse({"error": "Amount must be positive"}, status=400)
                converted_czk = round(amount * rate, 2)
                return JsonResponse({
                    "amount_eur": amount,
                    "converted_czk": converted_czk,
                    "rate": rate
                })
            except ValueError:
                return JsonResponse({"error": "Invalid amount"}, status=400)

        # If there is no amount parameter, we simply return the rate
        return JsonResponse({"rate": rate})

    except requests.RequestException as exc:
        return JsonResponse({"error": "Request failed", "details": str(exc)}, status=500)

def convert_view(request):
    return render(request, 'convert.html')


