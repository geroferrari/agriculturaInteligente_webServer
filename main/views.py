from asyncio.windows_events import NULL
from django.shortcuts import render
from fuzzyLogic.thread import CreateFuzzyThread
from sensors.thread import CreateMqttThread
from configuration.models import ConfigurationFieldModel 
from django.db import connection
import fnmatch


def home(request):

    # si el usuario configuro los datos iniciales, los obtengo 
    if  ConfigurationFieldModel.objects.exists() == 1:

        #CreateFuzzyThread().start()
        #CreateMqttThread().start()

        ConfigurationFieldValues=ConfigurationFieldModel.objects.all()
        sensores= ConfigurationFieldModel.objects.first()
        i = 0
        tables_data ={}
        sensors_data ={}
        print_data ={}
        #creo un objeto con la ultima fila de datos de cada tabla de cada sensor para mostrar en pantalla.
        if sensores.cantidad_sensores != NULL:
            cursor = connection.cursor()
            db_query = "SELECT name FROM sqlite_master WHERE type='table'"
            cursor.execute(db_query)
            tables_data[i]= cursor.fetchall()

            sensors_table= {}
            i = 0

            for n in tables_data[0]:
                if fnmatch.filter(n, 'sensor*'):
                    sensor_string =  str(fnmatch.filter(n, 'sensor*'))
                    sensors_table[i] = sensor_string[2:-2]
                    i+=1
                    
            i = 0
            #tengo que pensar como veo que tablas hay. aca estoy buscando la tabla sensor1 que ya no tengo mas, seria sensor0x0007
            while i < sensores.cantidad_sensores:

                sensor_query = f"SELECT sensorId, humedad, bateria, estado, tiempoMuestreo FROM {sensors_table[i]} ORDER BY id DESC LIMIT 1"
                cursor.execute(sensor_query)
                sensors_data[i]= cursor.fetchall()
                if not sensors_data[i]:
                    print_data[i] = {"sensorId" : "No Data", 
                                "humedad" :"No Data", 
                                "bateria" :"No Data", 
                                "tiempoMuestreo" :"No Data", 
                                "estado" : "No Data"} 
                else:
                    print_data[i] = {"sensorId" : sensors_data[i][0][0], 
                                    "humedad" : sensors_data[i][0][1], 
                                    "bateria" : sensors_data[i][0][2], 
                                    "estado" : sensors_data[i][0][3], 
                                    "tiempoMuestreo" : sensors_data[i][0][4]} 

                i=i+1

            return render(request, "home/home.html", {'ConfigurationFieldValues': ConfigurationFieldValues, 'sensorsData': print_data})

        return render(request, "home/home.html", {'ConfigurationFieldValues': ConfigurationFieldValues})

    return render(request, "home/home.html", {'ConfigurationFieldValues': ""})
