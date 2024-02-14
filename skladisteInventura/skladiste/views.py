from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
# Create your views here.

class HomePage(TemplateView):
    template_name="home.html"

class SignUpView(CreateView):
    form_class =UserCreationForm
    success_url=reverse_lazy("login")
    template_name="registration/signup.html"