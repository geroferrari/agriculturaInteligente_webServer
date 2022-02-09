import threading
from time import sleep
from irrigation.views import irrigation
from irrigation.models import *
from configuration.models import *
from datetime import datetime
from fuzzyLogic.views import fuzzyLogic 


class CreateFuzzyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.started = datetime.now()

    def run(self):
        try:
            i=1
            while (i == 1):
                irrigationValues=irrigationModel.objects.get(id = 1)
                configurationFieldValues=ConfigurationFieldModel.objects.get(id = 1)
                humidity_obtain=3
                weather_rain=4
                fuzzyInputData = {"temperature_min": configurationFieldValues.temperatura_minima_local, 
                                    "temperature_max": configurationFieldValues.temperatura_maxima_local,
                                    "humidity_min": configurationFieldValues.humedad_minima_local,
                                    "humidity_max": configurationFieldValues.humedad_maxima_local,
                                    "humidity_required": configurationFieldValues.humedad_requerida_local,
                                    "irrigation_max": irrigationValues.tiempo_maximo_riego,
                                    "irrigation_automatic": irrigationValues.automatico,
                                    "rain_offset": irrigationValues.cantidad_dias_sin_lluvia
                                    }
                if fuzzyInputData["humidity_required"] > humidity_obtain & fuzzyInputData["rain_offset"] < weather_rain:                   
                    fuzzyLogic(fuzzyInputData)
                    
                sleep(3600)
            
        except Exception as e:
            print(e)
