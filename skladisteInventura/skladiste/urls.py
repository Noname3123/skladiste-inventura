"""
URLs for app skladiste
"""
from django.contrib import admin
from django.urls import path, include

from skladiste.views import (HomePage, SignUpView, ProizvodView,TipProizvodaView, JediniceMjereView,ProizvodCreateView,ProizvodUpdateView,ProizvodDeleteView
, TipProizvodCreateView, TipProizvodUpdateView , TipProizvodDeleteView
,MjeraCreateView, MjeraUpdateView, MjeraDeleteView)

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("signup", SignUpView.as_view(),name="signup"),
    path("proizvodi", ProizvodView.as_view(), name="proizvodi"),
    path("kategorije", TipProizvodaView.as_view(),name="kategorije"),
    path("jedinice", JediniceMjereView.as_view(),name="jedinice_mjere"),
    path("novi_proizvod", ProizvodCreateView.as_view(), name="novi_proizvod"),
    path("update_proizvod\<int:pk>", ProizvodUpdateView.as_view(), name="update_proizvod"),
    path("delete_proizvod\<int:pk>", ProizvodDeleteView.as_view(), name="delete_proizvod"),
    path("nova_jedinica", MjeraCreateView.as_view(), name="nova_jedinica"),
    path("update_jedinica\<int:pk>", MjeraUpdateView.as_view(), name="update_jedinica"),
    path("delete_jedinica\<int:pk>", MjeraDeleteView.as_view(), name="delete_jedinica"),
    path("novi_tip", TipProizvodCreateView.as_view(), name="novi_tip"),
    path("update_tip\<int:pk>", TipProizvodUpdateView.as_view(), name="update_tip"),
    path("delete_tip\<int:pk>", TipProizvodDeleteView.as_view(), name="delete_tip"),

]
