from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from cars_vw.forms import CarModelForm
from cars_vw.models import Car, CarModel, CarColor
from users.models import Address


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
        context["colors"] = CarColor.objects.filter(cars__model=self.object).distinct()
        get_address_ = Address.objects.filter(cars__model=self.object).first()
        context["address"] = get_address_
        print(context["address"])
        if context["colors"]:
            default_color_ = context['colors'][0]
            context["cars"] = Car.objects.filter(model=self.object, color=default_color_)
        else:
            context["cars"] = Car.objects.filter(model=self.object)

        context["selected_car"] = context["cars"].first()

        #print(self.object)
        return context



class CarFilterView(DetailView):
    def post(self, request, *args, **kwargs):
        #context = self.get_context_data(**kwargs)
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

        print(context["address"])

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
