from django.urls import path
from . import views

urlpatterns = [
    path('', views.sensors, name="sensors"),
    path('population-chart/', views.population_chart, name='population-chart'),
]
