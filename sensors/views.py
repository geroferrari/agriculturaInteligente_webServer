from django.shortcuts import render
from configuration.models import ConfigurationFieldModel
from django.db import connection
from django.http import JsonResponse


def sensors(request):
    return render(request, "sensors/sensors.html")

def population_chart(request):

    json_data = {}
    sensores= ConfigurationFieldModel.objects.first()

    i = 1
    sensor ={}
    sensors_data ={}

    while i <= sensores.cantidad_sensores:
        sensor[i] = "Sensor0x00008"
        cursor = connection.cursor()
        query = "SELECT humedad, date FROM sensor0x00008" 
        cursor.execute(query)
        sensors_data[i]= cursor.fetchall()
        labels = []
        data = []
        for entry in sensors_data[i]:
            labels.append(entry[1].strftime("%Y-%m-%d, %H:%M"))
            data.append(entry[0])

        json_data[i] = {
        'labels': labels,
        'data': data,  
        }  
        i=i+1
    
    data_to_send = {
        'data1' : json_data[1]
    }


    return JsonResponse(data_to_send)


