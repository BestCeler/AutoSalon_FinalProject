from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cars_vw.forms import CarModelForm
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


class CarCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CarModelForm      # TODO add to form.py
    success_url = reverse_lazy('cars')
    permission_required = 'cars_vw.add_car'

    def form_invalid(self, form):
        print("Form 'CreatorModelForm' is not valid.")
        return super().form_invalid(form)


class CarUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CarModelForm
    model = Car
    success_url = reverse_lazy('cars')
    permission_required = 'cars_vw.change_car'

    def form_invalid(self, form):
        print("Form 'CreatorModelForm' is not valid.")
        return super().form_invalid(form)


class CarDeleteView(#StaffRequiredMixin,
        PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Car
    success_url = reverse_lazy('cars')
    permission_required = 'cars_vw.delete_car'
