
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CustomerView.as_view()),
    ]
