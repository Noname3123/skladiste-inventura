from django.shortcuts import render, redirect
from skladiste.forms import SignUpForm
from skladiste.models import Proizvod, Tip_Proizvoda, Jedinica_Mjere
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView
# Create your views here.

class HomePage(TemplateView):
    template_name="home.html"

class SignUpView(CreateView):
    form_class =SignUpForm
    success_url=reverse_lazy("login")
    template_name="registration/signup.html"


class ProizvodView(ListView):
    model=Proizvod
    template_name='proizvodList/proizvodi_list.html'
    context_object_name='proizvodi'

    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)

class TipProizvodaView(ListView):
    model=Tip_Proizvoda
    template_name='proizvodList/kategorije_list.html'
    context_object_name='tipovi'

    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)


class JediniceMjereView(ListView):
    model=Jedinica_Mjere
    template_name='proizvodList/jedinice_list.html'
    context_object_name='jedinice'

    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)
Jedinica_Mjere

