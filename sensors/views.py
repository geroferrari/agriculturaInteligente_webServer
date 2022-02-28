from django.shortcuts import render
from configuration.models import ConfigurationFieldModel
from django.db import connection
from django.http.response import JsonResponse
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
        sensor[i] = "Sensor" + str(i)
        cursor = connection.cursor()
        query = "SELECT humedad, date FROM " + sensor[i] 
        cursor.execute(query)
        sensors_data[i]= cursor.fetchall()

        labels = []
        data = []
        for entry in sensors_data[i]:
            labels.append(entry[1])
            data.append(entry[0])

        json_data[i] = {
        'labels': labels,
        'data': data,  
        }  
        i=i+1
    
    data_to_send = {
        'data1' : json_data[1],
        'data2' : json_data[2]
    }


    return JsonResponse(data_to_send)


