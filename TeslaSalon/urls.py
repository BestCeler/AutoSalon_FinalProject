"""
URL configuration for TeslaSalon2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from cars_vw.views import *
from orders.views import  *
#from orders.views import MakeOrderView
from users.views import SubmittableLoginView, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path("user/login/", SubmittableLoginView.as_view(), name="login"),
    path("user/signup/", SignUpView.as_view(), name="signup"),

    path('models/', ModelsListView.as_view(), name='models'),
    path('model/<int:pk>/', CarToModelDetailView.as_view(), name='model'),
    path('model//create/', ModelCreateView.as_view(), name='model_create'),
    path('model/update/<int:pk>/',ModelUpdateView.as_view(), name='model_update'),
    path('model/delete/<int:pk>/', ModelDeleteView.as_view(), name='model_delete'),

    path("model/color/filter", CarFilterView.as_view(), name='car_filter'),
    #path("order/new/", MakeOrderView.as_view(), name='order_new'),
    path("order/make", OrdersActions.as_view(), name='make_order'),
    path("order/process/<int:pk>", OrderDetailView.as_view(), name='order_process'),



]
