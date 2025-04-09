from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cars_vw.models import Car


# Create your views here.

def home(request):
    return render(request, 'home.html')


class CarsListView(ListView):
    template_name = 'cars.html'
    model = Car
    context_object_name = 'cars'

class CarDetailView(DetailView):
    template_name = 'car.html'
    model = Car
    context_object_name = 'car'