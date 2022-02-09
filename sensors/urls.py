from django.urls import path

from . import views

urlpatterns = [
    path('', views.sensors, name="sensors"),
    path('api/data/sensor0', views.get_data_sensor0, name="api-data-sensor0" ),
    path('api/data/sensor1', views.get_data_sensor1, name="api-data-sensor1" ),
]
