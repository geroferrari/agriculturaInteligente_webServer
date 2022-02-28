from django.shortcuts import render
from .models import irrigationModel
from fuzzyLogic.models import irrigationHistoryModel


def irrigation(request):

    if request.method == "POST":
        data=request.POST
        irrigationValues=irrigationModel.objects.get(id=1)
        irrigationValues.automatico =  request.POST.get("automatico", "off")
        irrigationValues.encendido = request.POST.get("encendido", "off")
        irrigationValues.riego_diurno = request.POST.get("riego_diurno", "off")
        irrigationValues.tiempo_maximo_riego = int(data["tiempo_maximo_riego"])
        irrigationValues.envio_alertas = request.POST.get("envio_alertas", "off")
        irrigationValues.cantidad_dias_sin_lluvia = int(data["cantidad_dias_sin_lluvia"])
        irrigationValues.save()

    irrigationValues=irrigationModel.objects.all()
    irrigationHistoryValues=irrigationHistoryModel.objects.all()


    return render(request, "irrigation/irrigation.html", {"irrigationValues": irrigationValues, "irrigationHistory" : irrigationHistoryValues})