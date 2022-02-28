import threading
from time import sleep
from .forms import irrigationHistoryForm
from .models import irrigationHistoryModel
from irrigation.models import *
from configuration.models import *
from datetime import datetime
from fuzzyLogic.views import fuzzyLogic 
from weatherAPI.views import temperatureAPIData, rainAPIData

class CreateFuzzyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.started = datetime.now()

    def run(self):
        try:
            a = 0
            while True:
                humidity_measured = 10
                humidity_min = 10
                humidity_max = 20
                humidity_required = 15
                temperature_min = 20                                                             
                temperature_max = 30                                                               
                temperature= 25                                                               
                tiempo_maximo_riego = 90
                #algoritmo convergente:
                step_number = 0
                humidity_diference = 0
                last_max_duration = 0

                irrigationHistoryValues = irrigationHistoryModel.objects.all().order_by('-id')

                humidity_diference = 100   
                last_max_duration = tiempo_maximo_riego

                for s in irrigationHistoryValues:
                    print("****************", s.duracion_maxima, "********")
                    #busco casos donde la humedad sea la misma o varie en un +-10% y la temperatura +-20%
                    if abs(s.humedad_antes - humidity_measured) <= round(humidity_measured*0.05): 
                        if abs(s.temperatura - round(temperature)) <= round(temperature*0.2): 
                            if abs(s.humedad_despues - humidity_required) > round(humidity_required*0.1):
                                #en el primer caso donde esto ocurra, deberia salir del for con eltiempo utilizado y el numero de paso
                                
                                last_max_duration = s.duracion_maxima
                                humidity_diference = s.humedad_despues - humidity_required
                                step_number = s.numero_paso

                                print("------------------------------------")
                                print("Se encontro un caso similar en la BD ")
                                print("Duracion maxima previa: ", last_max_duration)
                                print("Diferencia con la humedad requerida: ", humidity_diference)
                                print("Numero de Paso: ", step_number)
                                print("------------------------------------")

                                break
                            else:
                                humidity_diference = s.humedad_despues - humidity_required
                                last_max_duration = s.duracion_maxima
                                step_number = 1000
                                print("------------------------------------")
                                print("Se encontro un caso donde la diferencia de humedad es < 10%")
                                print("Duracion maxima previa: ", last_max_duration)
                                print("Diferencia con la humedad requerida: ", humidity_diference)
                                print("Numero de Paso: ", step_number)
                                print("------------------------------------")
                                break
                    else:
                        print("------------------------------------")
                        print("No se encontro ninguna coincidencia, se usa el maximo tiempo de riego")
                        print("------------------------------------")
                        last_max_duration = tiempo_maximo_riego
                        break


                duration_percentage_update = 0

                if step_number == 1000:
                    print("------------------------------------")
                    print("Estoy en el step 1000, se mantiene el tiempo de riego")
                    print("------------------------------------")

                elif step_number == 0:
                    print("------------------------------------")
                    print("Estoy en el step 0")
                    print("------------------------------------")

                    step_number += 1
                    # si es distinto de cero, signifca que ya hay un stepnumber, entoces calculo el valor    
                else:
                    duration_percentage_update = 0.1 - (step_number*0.01)
                    duration_percentage_update = duration_percentage_update * (1 - step_number*0.1)
                    print("------------------------------------")
                    print("Estoy en algun step", step_number-1, "se cambian en un", duration_percentage_update, "%")
                    print("------------------------------------")
                    step_number +=1

                    #actualizo la maxima duración del algoritmo para obtener una respuesta mas certera
                if humidity_diference < 0:
                    last_max_duration = last_max_duration + last_max_duration * duration_percentage_update
                    print("------------------------------------")
                    print("Me habia quedado corto - La maxima duracion es ahora",  last_max_duration)
                    print("------------------------------------")

                elif humidity_diference == 0: 
                    print("------------------------------------")
                    print("Se deberia repetier la maxima duracion anterior, la humedad es la correcta")
                    print("------------------------------------")

                else:
                    last_max_duration = last_max_duration - last_max_duration * duration_percentage_update
                    print("------------------------------------")
                    print("Me habia pasado - La maxima duracion es ahora", last_max_duration)
                    print("------------------------------------")

                                
                fuzzyInputData = {  "humidity_min": humidity_min,
                                "humidity_max": humidity_max,
                                "humidity_required": humidity_required,
                                "irrigation_max": last_max_duration,
                                "temperature_min": temperature_min,                                                                
                                "temperature_max": temperature_max,                                                                
                                "temperature": temperature,                                                                
                                "humidity_measured": humidity_measured,                                                                
                                }

                irrigation_time = fuzzyLogic(fuzzyInputData)

                #comunicacion con la valvula para enviarle el tiempo que va a tener que permanecer abierta

                #hacer llamada a los sensores para ver los datos nuevos, capaz tengo que hacer un wait 
                # para esperar que me lleguen los valores, preguntando si los que tengo son distinto a los anteriores
                caudal_measured = 400
                humidity_measured_new = [30,26,24,22,20,18, 5, 10, 13, 15, 15, 15]
                data = {
                "duracion": round(irrigation_time["Time"]),
                "duracion_maxima": round(last_max_duration),
                "cantidad_agua": round(caudal_measured),
                "humedad_antes": round(humidity_measured),
                "humedad_despues": round(humidity_measured_new[a]),
                "temperatura": temperature,
                "numero_paso": step_number
                }

                a+=1


                irrigationHistoryValues=irrigationHistoryForm(data)
                irrigationHistoryValues.save()

        except Exception as e:
            print(e)
