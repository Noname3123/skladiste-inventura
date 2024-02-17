"""
URLs for app skladiste
"""
from django.contrib import admin
from django.urls import path, include

from skladiste.views import HomePage, SignUpView, ProizvodView,TipProizvodaView, JediniceMjereView,ProizvodCreateView

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("signup", SignUpView.as_view(),name="signup"),
    path("proizvodi", ProizvodView.as_view(), name="proizvodi"),
    path("kategorije", TipProizvodaView.as_view(),name="kategorije"),
    path("jedinice", JediniceMjereView.as_view(),name="jedinice_mjere"),
    path("novi_proizvod", ProizvodCreateView.as_view(), name="novi_proizvod"),

]
