from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from .forms import ConfigurationFieldForm
from django.db import connection
from .models import ConfigurationFieldModel

def configuration_field(request):

    if request.method == "POST":
        data=request.POST

        if  ConfigurationFieldModel.objects.exists() == 1:

            ConfigurationFieldValues = ConfigurationFieldModel.objects.get(id = 1)

            if ConfigurationFieldValues.cantidad_sensores < int(data['cantidad_sensores']):
                i = ConfigurationFieldValues.cantidad_sensores + 1
                while i < int(data['cantidad_sensores']):
                    sensor = "sensor" + str(i)
                    cursor = connection.cursor()
                    database_name = "CREATE TABLE " + str(sensor) + " (Id int(11), humedad int(4), bateria int(4), estado boolean, date datetime )"
                    cursor.execute(database_name)
                    cursor.close()
                    i=i+1

            ConfigurationFieldValues.nombre_campo = data["nombre_campo"]
            ConfigurationFieldValues.provincia = data["provincia"]
            ConfigurationFieldValues.ciudad = data["ciudad"]
            ConfigurationFieldValues.latitud = data["latitud"]
            ConfigurationFieldValues.longitud = data["longitud"]
            ConfigurationFieldValues.temperatura_minima_local = int(data["temperatura_minima_local"])
            ConfigurationFieldValues.temperatura_maxima_local = int(data["temperatura_maxima_local"])
            ConfigurationFieldValues.humedad_maxima_local = int(data["humedad_maxima_local"])
            ConfigurationFieldValues.humedad_minima_local = int(data["humedad_minima_local"])
            ConfigurationFieldValues.humedad_requerida_local = int(data["humedad_requerida_local"])
            ConfigurationFieldValues.cultivo = data["cultivo"]
            ConfigurationFieldValues.cantidad_sensores = int(data["cantidad_sensores"])
            ConfigurationFieldValues.area_cubierta = int(data["area_cubierta"])
    
            ConfigurationFieldValues.save()

        else:
            data = request.POST
            ConfigurationFieldValues=ConfigurationFieldForm(data)
            ConfigurationFieldValues.save()

            i = 1
            while i < int(data['cantidad_sensores']):
                sensor = "sensor" + str(i)
                cursor = connection.cursor()
                database_name = "CREATE TABLE " + str(sensor) + " (Id int(11), humedad int(4), bateria int(4), estado boolean, date datetime )"
                cursor.execute(database_name)
                cursor.close()
                i=i+1
        
        return render(request, "configuration/configuration_field_completed.html", {'ConfigurationFieldValues': ConfigurationFieldValues})

    else: 
        rows=ConfigurationFieldModel.objects.count()
        if rows == 1:
            ConfigurationFieldValues=ConfigurationFieldModel.objects.all()
            return render(request, "configuration/configuration_field_completed.html", {'ConfigurationFieldValues': ConfigurationFieldValues})
        else:
            ConfigurationFieldValues=ConfigurationFieldForm()
            return render(request, "configuration/configuration_field.html", {'ConfigurationFieldValues': ConfigurationFieldValues})
