from django.urls import path

from . import views

urlpatterns = [
    path('', views.irrigation, name="irrigation"),
    path('irrigation-chart/', views.irrigation_chart, name='irrigation-chart'),
]
