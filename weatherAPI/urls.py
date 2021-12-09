from django.urls import path
from . import views

urlpatterns = [
    path('realTimeWeather.html', views.realTimeWeather ),
]
