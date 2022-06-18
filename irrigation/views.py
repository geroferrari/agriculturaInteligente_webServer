from django.http import JsonResponse
from django.shortcuts import render
from .models import irrigationModel
from fuzzyLogic.models import irrigationHistoryModel
from django.db import connection


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

def irrigation_chart(request):

    irrigation_data ={}
    cursor = connection.cursor()
    cursor.execute(f"SELECT fecha, duracion, cantidad_agua, humedad_antes, humedad_despues, duracion_maxima FROM fuzzyLogic_irrigationhistorymodel")
    
    irrigation_data= cursor.fetchall()
    
    labels = []
    duracion = []
    cantidad_agua = []
    humedad_antes = []
    humedad_despues = []
    duracion_maxima = []
    for entry in irrigation_data:
        labels.append(entry[0])
        duracion.append(entry[1])
        cantidad_agua.append(entry[2])
        humedad_antes.append(entry[3])
        humedad_despues.append(entry[4])
        duracion_maxima.append(entry[5])

    
    humedad_diferencia = {}
    humedad_diferencia = [humedad_antes,  humedad_despues]
    humedad_diferencia = [(y-x) for x,y in zip(*humedad_diferencia)]    

    json_data = {
    'labels': labels,
    'duracion': duracion,  
    'cantidad_agua': cantidad_agua,  
    'humedad_diferencia': humedad_diferencia,  
    'duracion_maxima': duracion_maxima
    }  
    cursor.close()

    return JsonResponse(json_data)


