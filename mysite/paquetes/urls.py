
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.PaqueteView.as_view()),
    path('obtenerTotalPorFecha/', views.obtenerTotalPorFecha, name="obtenerTotalPorFecha")
    ]
