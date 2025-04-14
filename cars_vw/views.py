from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from cars_vw.forms import CarModelForm
from cars_vw.models import Car, CarModel


# Create your views here.

def home(request):
    return render(request, 'home.html')


class CarsListView(ListView):
    template_name = 'cars.html'
    model = CarModel
    context_object_name = 'cars'


"""class CarDetailView(DetailView):
    template_name = 'car.html'
    model = CarModel
    context_object_name = 'car' # TODO: change into model - we need to change a lot of things to models not cars"""


class CarToModelDetailView(DetailView):
    template_name = 'car.html'
    model = CarModel
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["models"] = CarModel.objects.get(self.request.META)
        context["cars"] = Car.objects.filter(model=self.object)
        #print(self.object)
        return context


def car_filter(request):
    if request.method == "POST":
        filtered_cars = Car.objects.filter(request.post.get())

        context = {"cars": filtered_cars}



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
