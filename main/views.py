from django.shortcuts import render
from fuzzyLogic.thread import CreateFuzzyThread
from sensors.thread import CreateMqttThread
from configuration.models import ConfigurationFieldModel 
from django.db import connection

def home(request):
    CreateFuzzyThread().start()
    #CreateMqttThread().start()

    if  ConfigurationFieldModel.objects.exists() == 1:
        ConfigurationFieldValues=ConfigurationFieldModel.objects.all()
        sensores= ConfigurationFieldModel.objects.first()

        i = 1
        sensor ={}
        sensors_data ={}
        print_data ={}
        while i <= sensores.cantidad_sensores:
            sensor[i] = "Sensor" + str(i)
            cursor = connection.cursor()
            query = "SELECT humedad, bateria, estado FROM " + sensor[i] +  " ORDER BY id DESC LIMIT 1"
            cursor.execute(query)
            sensors_data[i]= cursor.fetchall()
            print_data[i] = {"humedad" : sensors_data[i][0][0], 
                             "bateria" : sensors_data[i][0][1], 
                             "estado" : sensors_data[i][0][2]} 
            i=i+1

        return render(request, "home/home.html", {'ConfigurationFieldValues': ConfigurationFieldValues, 'sensorsData': print_data})

    return render(request, "home/home.html")
