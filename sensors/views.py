from django.shortcuts import render
from matplotlib.pyplot import table
from configuration.models import ConfigurationFieldModel
from django.db import connection
from django.http import JsonResponse
import numpy as np

def sensors(request):

    return render(request, "sensors/sensors.html")

def population_chart(request):

    json_data = {}
    sensores= ConfigurationFieldModel.objects.first()

    i = 0
    n = 0
    sensor ={}
    sensors_data ={}
    name = "sensor0x000"
    cantidad_tablas = sensores.cantidad_sensores
    while  i < 11:
        tablename = name + (str(i) if i/10>=1 else "0" + str(i))
        cursor = connection.cursor()
        db_query = " SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + tablename + "' " 
        cursor.execute(db_query)
        if cursor.fetchone()[0]==1:
            cursor.execute(f"SELECT humedad, date, bateria FROM {tablename}")
            sensors_data[i]= cursor.fetchall()
            labels = []
            data = []
            battery = []
            for entry in sensors_data[i]:
                labels.append(entry[1])
                data.append(entry[0])
                battery.append(entry[2])
            json_data[i] = {
            'labels': labels,
            'data': data,  
            'battery': battery,  
            }  
            cantidad_tablas-=1
            cursor.close()
        i=i+1
    

    promedio_hum = {}
    promedio_hum = [json_data[8]['data'],  json_data[9]['data']]
    promedio_hum = [(x+y)/2 for x,y in zip(*promedio_hum)]

    promedio_bat = {}
    promedio_bat = [json_data[8]['battery'],  json_data[9]['battery']]
    promedio_bat = [(x+y)/2 for x,y in zip(*promedio_bat)]


    data_to_send = {
        'data1' : json_data[8],
        'data2' : json_data[9],
        'data3' : promedio_hum,
        'data4' : promedio_bat
    }


    return JsonResponse(data_to_send)


