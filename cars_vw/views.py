from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from cars_vw.forms import CarModelForm
from cars_vw.models import Car, CarModel, CarColor


# Create your views here.

def home(request):
    return render(request, 'home.html')


class ModelsListView(ListView):
    template_name = 'models.html'
    model = CarModel
    context_object_name = 'models'


"""class CarDetailView(DetailView):
    template_name = 'model.html'
    model = CarModel
    context_object_name = 'car' # TODO: change into model - we need to change a lot of things to models not cars"""


class CarToModelDetailView(DetailView):
    template_name = 'model.html'
    model = CarModel
    context_object_name = 'model'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["models"] = CarModel.objects.get(self.request.META)
        context["cars"] = Car.objects.filter(model=self.object)
        context["colors"] = CarColor.objects.filter(cars__model=self.object).distinct()
        #print(self.object)
        return context

    def post(self, request, *args, **kwargs):
        model_ = request.POST.get("model")
        color_ = request.POST.get("color")
        filtered_cars = Car.objects.filter(color=color_ ,model=model_)

        context = {"cars": filtered_cars}
        print(model_)
        return render(request, "model.html", context)


class CarFilterView(ListView):
    template_name = 'model.html'
    #model = CarModel
    context_object_name = 'model'
    def post(self, request, *args, **kwargs):
        model_ = request.POST.get("model")
        color_ = request.POST.get("color")
        filtered_cars = Car.objects.filter(color=color_ ,model=model_)

        context = {"cars": filtered_cars}
        print(model_)
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
    model = Car
    success_url = reverse_lazy('models')
    permission_required = 'cars_vw.change_car'

    def form_invalid(self, form):
        print("Form 'CreatorModelForm' is not valid.")
        return super().form_invalid(form)


class ModelDeleteView(#StaffRequiredMixin,
        PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Car
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