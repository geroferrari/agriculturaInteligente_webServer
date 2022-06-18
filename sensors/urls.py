from django.urls import path
from . import views

urlpatterns = [
    path('', views.sensors, name="sensors"),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('population-chart-2/', views.population_chart, name='population-chart-2'),
]
