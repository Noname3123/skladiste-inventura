"""
URLs for app skladiste
"""
from django.contrib import admin
from django.urls import path, include

from skladiste.views import HomePage, SignUpView, ProizvodView

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("signup", SignUpView.as_view(),name="signup"),
    path("proizvodi", ProizvodView.as_view(), name="proizvodi")
]
