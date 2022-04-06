from django.shortcuts import render, redirect
from .forms import ConfigurationFieldForm
from .models import ConfigurationFieldModel
from irrigation.models import irrigationModel

def configuration_field(request):

    if request.method == "POST":
        data=request.POST

        if  ConfigurationFieldModel.objects.exists() == 1:

            ConfigurationFieldValues = ConfigurationFieldModel.objects.get(id = 1)

            ConfigurationFieldValues.id = data["id"]
            ConfigurationFieldValues.nombre_campo = data["nombre_campo"]
            ConfigurationFieldValues.provincia = data["provincia"]
            ConfigurationFieldValues.ciudad = data["ciudad"]
            ConfigurationFieldValues.humedad_maxima_local = int(data["humedad_maxima_local"])
            ConfigurationFieldValues.humedad_minima_local = int(data["humedad_minima_local"])
            ConfigurationFieldValues.humedad_requerida_local = int(data["humedad_requerida_local"])
            ConfigurationFieldValues.cultivo = data["cultivo"]
            ConfigurationFieldValues.area_cubierta = int(data["area_cubierta"])
    
            ConfigurationFieldValues.save()

        else:
            data = request.POST
            ConfigurationFieldValues=ConfigurationFieldForm(data)
            ConfigurationFieldValues.save()

            irrigationValues=irrigationModel()
            irrigationValues.id = 1
            irrigationValues.automatico = "off"
            irrigationValues.encendido = "off"
            irrigationValues.riego_diurno = "off"
            irrigationValues.tiempo_maximo_riego = 60
            irrigationValues.envio_alertas = "off"
            irrigationValues.cantidad_dias_sin_lluvia = 0
            irrigationValues.save()

        return render(request, "home/home.html")

    else: 
        rows=ConfigurationFieldModel.objects.count()
        if rows == 1:
            ConfigurationFieldValues=ConfigurationFieldModel.objects.all()
            return render(request, "configuration/configuration_field.html", {'ConfigurationFieldValues': ConfigurationFieldValues})
        else:
            ConfigurationFieldValues=ConfigurationFieldForm()
            return render(request, "configuration/configuration_field.html")
