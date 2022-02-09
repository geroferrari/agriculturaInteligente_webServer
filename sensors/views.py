from django.shortcuts import render
from configuration.models import ConfigurationFieldModel
from django.db import connection
from django.http.response import JsonResponse
from django.shortcuts import  HttpResponse
from django.http import JsonResponse


def sensors(request):
    sensores= ConfigurationFieldModel.objects.first()
    cursor = connection.cursor()
    i = 0
    sensor ={}

    while i < sensores.cantidad_sensores:
        sensor[i] = "Sensor " + str(i)
        i=i+1

   # i=0 
   # while i < 
   # database_name = "SELECT * FROM sensor" + str(i) 
   # cursor.execute(database_name)

    return render(request, "sensors/sensors.html", {"sensor": sensor})



def get_data_sensor0(request, *args, **kwargs):
    labels =  ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    default_items = [123, 2, 43, 532, 23, 2] 
    data = {
        "labels" : labels,
        "default": default_items,
    }
    return JsonResponse(data)

def get_data_sensor1(request, *args, **kwargs):
    labels =  ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    default_items = [123, 2, 43, 532, 23, 2] 
    data = {
        "labels" : labels,
        "default": default_items,
    }
    return JsonResponse(data)
