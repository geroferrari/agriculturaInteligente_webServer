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
            i=1
            while (i == 1):
                sleep(3600)

                #data from configuration
                irrigationValues=irrigationModel.objects.get(id = 1)
                configurationFieldValues=ConfigurationFieldModel.objects.get(id = 1)

                #verifico que el riego no este encendido
                print("------------------------------------------------")
                print("[info] Verificando si el riego esta prendido...")
                if irrigationValues.encendido == "on":
                    print("[info] Riego Encendido - No enciendo riego")
                    continue

                print("[info] Riego apagado")
                print("------------------------------------------------")

                #verifico que este activado el modo automatico
                print("[info] Verificando si el riego automatico esta autorizado...")
                if irrigationValues.automatico == "off":
                    print("[info] Riego Automatico apagado")
                    continue

                print("[info] Riego Automatico apagado")
                print("------------------------------------------------")

                #data from sensors and api
                #la humedad actual entregafa por los sensores, deberia hacer un promedio entre todos
                #la temperatura actual, minima y maxima de la api del clima
                #si llueve o no los proximos X dias
                
                #verifico que la humedad sea menor al minimo establecido por el usuario
                print("[info] Verificando si la humedad medida < humedad minima...")
                humidity_measured = 10
            
                if humidity_measured > configurationFieldValues.humedad_minima_local:
                    print("[info] Humedad mayor a la minima")
                    continue

                print("[info] Humedad menor a la minima")
                print("------------------------------------------------")

                #verifico que no sea de dia. 

                temperature_data = temperatureAPIData()
                print("[info] Verificando si es de dia y se permite regar...")

                if irrigationValues.riego_diurno == "off":
                    if datetime.now().timestamp() > temperature_data["sunrise"] and datetime.now().timestamp() < temperature_data["sunset"] :
                        print("[info] es de dia - no se puede regar")
                        continue
                print("[info] Es de noche / se permite el riego diurno")

                print("------------------------------------------------")

                print("[info] Verificando si llovera en los proximos dias...")
                #verifico que no llueva por los proximos X dias 
                if rainAPIData(irrigationValues.cantidad_dias_sin_lluvia) == True:
                    print("[info] va a llover - no se regará")
                    continue
                
                print("[info] No va a llover")

                print("------------------------------------------------")

                
                #algoritmo convergente:
                step_number = 0
                last_humidity_diference = 0
                last_max_duration = 0

                irrigationHistoryValues = irrigationHistoryModel.objects.all().order_by('-id')
                for s in irrigationHistoryValues:
                    #busco casos donde la humedad sea la misma o varie en un +-5% y la temperatura +-10%
                    if abs(s.humedad_antes - humidity_measured) <= round(humidity_measured*0.05): 
                        if abs(s.temperatura - round(temperature_data["temperature"])) <= round(temperature_data["temperature"]*0.1): 
                            if abs(s.humedad_despues - configurationFieldValues.humedad_requerida_local) > round(configurationFieldValues.humedad_requerida_local*0.05):
                                #en el primer caso donde esto ocurra, deberia salir del for con el caudal de agua utilizado y el numero de paso
                                
                                last_max_duration = s.duracion_maxima

                                last_humidity_diference = s.humedad_despues - configurationFieldValues.humedad_requerida_local
                                step_number = s.numero_paso
                                break
                            else:
                               last_max_duration = s.duracion_maxima
                               step_number = 1000
                               break
                    else:   
                        last_max_duration = irrigationModel.tiempo_maximo_riego
                        break

                #si el stepnumber es 0 significa que no hya coincidencias entones, defino que el porcentaje de cambio del caudal
                #va a ser 10% y fijo el stepnumer en 1 para guardar en la base de datos

                duration_percentage_flag = 0


                if step_number == 1000:
                    duration_percentage_update = 0
                    break

                elif step_number == 0   :
                    duration_percentage_update = 0
                    step_number == 1

                # si es distinto de cero, signifca que ya hay un stepnumber, entoces calculo el valor    
                else:
                    if last_humidity_diference > 0  and step_number == 1 and duration_percentage_flag == 0:
                        duration_percentage_flag = 1
                        step_number = 1
                        duration_percentage_update = 0.1
                        #significa que me pase del valor en el primer intento, tengo que empezar a restar de a 10%

                    elif last_humidity_diference < 0 and step_number == 1 and duration_percentage_flag == 0:
                        duration_percentage_flag = 1
                        step_number = 1
                        duration_percentage_update = 0.1
                        #significa que con el tiempo actual no llegue al valor y tengo que subir de a 10%

                    elif last_humidity_diference > 0 and step_number!=1000 and duration_percentage_flag == 1:
                        step_number+=1
                        duration_percentage_update = duration_percentage_update - (duration_percentage_update * 0.1)
                        #significa que me pase del valor pero venia subiendo de a 10%, tengo que disminuir el porcentaje 
                    
                    elif last_humidity_diference < 0 and step_number!=1000 and duration_percentage_flag == 1: 
                        step_number += 1
                        duration_percentage_update = duration_percentage_update - (duration_percentage_update * 0.1)
                        #seria cuando ya me habia pasado y tengo que empezar a retroceder bajando el %



                #actualizo la maxima duración del algoritmo para obtener una respuesta mas certera
                if last_humidity_diference < 0:
                    last_max_duration = last_max_duration + last_max_duration * duration_percentage_update
                elif last_humidity_diference == 0: 
                   last_max_duration = int(irrigationValues.tiempo_maximo_riego)
                else:
                    last_max_duration = last_max_duration - last_max_duration * duration_percentage_update


                fuzzyInputData = {  "humidity_min": configurationFieldValues.humedad_minima_local,
                                    "humidity_max": configurationFieldValues.humedad_maxima_local,
                                    "humidity_required": configurationFieldValues.humedad_requerida_local,
                                    "irrigation_max": last_max_duration,
                                    "temperature_min": round(temperature_data["temperature_min"]),                                                                
                                    "temperature_max": round(temperature_data["temperature_max"]),                                                                
                                    "temperature": round(temperature_data["temperature"]),                                                                
                                    "humidity_measured": humidity_measured,                                                                
                                    }
                
                irrigation_time = fuzzyLogic(fuzzyInputData)
                
                #comunicacion con la valvula para enviarle el tiempo que va a tener que permanecer abierta

                #hacer llamada a los sensores para ver los datos nuevos, capaz tengo que hacer un wait 
                # para esperar que me lleguen los valores, preguntando si los que tengo son distinto a los anteriores
                caudal_measured = 400
                humidity_measured_new = 20

                data = {
                    "duracion": round(irrigation_time["Time"]),
                    "duracion_maxima": round(last_max_duration),
                    "cantidad_agua": round(caudal_measured),
                    "humedad_antes": round(humidity_measured),
                    "humedad_despues": round(humidity_measured_new),
                    "temperatura": round(temperature_data["temperature"]),
                    "numero_paso": step_number
                }

                irrigationHistoryValues=irrigationHistoryForm(data)
                irrigationHistoryValues.save()


        except Exception as e:
            print(e)
