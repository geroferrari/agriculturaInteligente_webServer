from asyncio.windows_events import NULL
from django.shortcuts import render
from fuzzyLogic.thread import CreateFuzzyThread
from sensors.thread import CreateMqttThread
from configuration.models import ConfigurationFieldModel 
from django.db import connection

def home(request):

    # si el usuario configuro los datos iniciales, los obtengo 
    if  ConfigurationFieldModel.objects.exists() == 1:

        #CreateFuzzyThread().start()
        CreateMqttThread().start()

        ConfigurationFieldValues=ConfigurationFieldModel.objects.all()
        sensores= ConfigurationFieldModel.objects.first()

        i = 1
        sensor ={}
        sensors_data ={}
        print_data ={}
        #creo un objeto con la ultima fila de datos de cada tabla de cada sensor para mostrar en pantalla.
        if sensores.cantidad_sensores != NULL:

            while i <= sensores.cantidad_sensores:
            #    sensor[i] = "Sensor" + str(i)
            #    cursor = connection.cursor()
            #    query = "SELECT sensorId, humedad, bateria, estado, tiempoMuestreo FROM " + sensor[i] +  " ORDER BY id DESC LIMIT 1"
            #    cursor.execute(query)
            #    sensors_data[i]= cursor.fetchall()
            #    print(sensors_data[i])
            #    if not sensors_data[i]:
                print_data[i] = {"sensorId" : "No Data", 
                                "humedad" :"No Data", 
                                "bateria" :"No Data", 
                                "tiempoMuestreo" :"No Data", 
                                "estado" : "No Data"} 
            #    else:
            #        print_data[i] = {"sensorId" : sensors_data[i][0][0], 
            #                        "humedad" : sensors_data[i][0][1], 
            #                        "bateria" : sensors_data[i][0][2], 
            #                        "estado" : sensors_data[i][0][3], 
            #                        "tiempoMuestreo" : sensors_data[i][0][4]} 

                i=i+1

            return render(request, "home/home.html", {'ConfigurationFieldValues': ConfigurationFieldValues, 'sensorsData': print_data})

        return render(request, "home/home.html", {'ConfigurationFieldValues': ConfigurationFieldValues})

    return render(request, "home/home.html", {'ConfigurationFieldValues': ""})
