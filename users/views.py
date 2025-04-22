from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from users.forms import SignupForm
from users.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'account_forms.html'


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))  # zůstat na stejné stránce


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'