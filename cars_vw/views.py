from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import BooleanField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cars_vw.forms import CarModelForm
from cars_vw.models import Car, CarModel


# Create your views here.

def home(request):
    return render(request, 'home.html')


class CarsListView(ListView):
    template_name = 'cars.html'
    model = CarModel
    context_object_name = 'cars'


class CarDetailView(DetailView):
    template_name = 'car.html'
    model = CarModel
    context_object_name = 'car'


class CarCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CarModelForm
    success_url = reverse_lazy('cars')
    permission_required = 'cars_vw.add_car'

    def form_invalid(self, form):
        print("Form 'CreatorModelForm' is not valid.")
        return super().form_invalid(form)


class CarUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CarModelForm
    model = CarModel
    success_url = reverse_lazy('cars')
    permission_required = 'cars_vw.change_car'

    def form_invalid(self, form):
        print("Form 'CreatorModelForm' is not valid.")
        return super().form_invalid(form)


class CarDeleteView(#StaffRequiredMixin,
        PermissionRequiredMixin, DeleteView):

    template_name = 'confirm_delete.html'
    model = CarModel
    success_url = reverse_lazy('cars')
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