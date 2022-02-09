from .forms import irrigationHistoryForm
from .fuzzy_system.fuzzy_system import FuzzySystem
from .fuzzy_system.fuzzy_variable_output import FuzzyOutputVariable
from .fuzzy_system.fuzzy_variable_input import FuzzyInputVariable


def fuzzyLogic(data):
	FuzzyInputVariableTemperature = "Temperature" 
	FuzzyInputVariableTemperature_min = data["temperature_min"]
	FuzzyInputVariableTemperature_max = data["temperature_max"] 
	FuzzyInputVariableTemperature_middle = (FuzzyInputVariableTemperature_min + FuzzyInputVariableTemperature_max)/2 

	FuzzyInputVariableSoilHumidity = "Soil Humidity" 
	FuzzyInputVariableSoilHumidity_min = data["humidity_min"] 
	FuzzyInputVariableSoilHumidity_required = data["humidity_required"]  
	FuzzyInputVariableSoilHumidity_max = data["humidity_max"]

	FuzzyOutputVariableIrrigation = "Water" 
	FuzzyOutputVariableIrrigation_min = 0
	FuzzyOutputVariableIrrigation_max = data["irrigation_max"]

	FuzzyVariable_step = 100  

	#booleano para saber si va a llover o no por los proximos X dias
	weatherVariable = data["rain_offset"]
	#Offset configurado por el usuario para que solo se riegue si la humedad registrada es menor a%
	irrigationOffset = data["humidity_min"] 


	# z/2 = y - x
	# z el rango total de temperaturas que se abarca
	# y es la longitud total de la base del triangulo, los tres triangulos seran iguales
	# x es la longitud de superposicion entre triangulos, el area de superposicion es siempre la misma

	# k = cte = z/2 = (|Temp min| + |temp maxima|)/2  
	#temperatureRangeLength =  (abs(FuzzyInputVariableTemperature_min) +  abs(FuzzyInputVariableTemperature_max))/2
	#soilHumidityRangeLength =  (abs(FuzzyInputVariableSoilHumidity_min) +  abs(FuzzyInputVariableSoilHumidity_max))/2

	# y = x + k
	# se elige un valor para x, a partir del cual se busca el valor de y
	# SE PEUDE IMPLEMENTAR UNA INTELIGENCIA ARTIFICIAL PARA IR CAMBIANDO EL VALOR DE X Y MEJORANDO EL SISTEMA???

	# temperatura
	#temperature_x = 15
	#temperature_y = temperatureRangeLength + temperature_x  #40

	#soilHumidity_x = 5
	#soilHumidity_y = soilHumidityRangeLength + soilHumidity_x  #40


	# Agua riego
	irrigation_x = 10
	irrigation_y = FuzzyOutputVariableIrrigation_max/4 + irrigation_x


	temperature = FuzzyInputVariable(FuzzyInputVariableTemperature,FuzzyInputVariableTemperature_min, FuzzyInputVariableTemperature_max, FuzzyVariable_step)
	temperature.add_triangular('cold', FuzzyInputVariableTemperature_min, FuzzyInputVariableTemperature_min, FuzzyInputVariableTemperature_middle)
	temperature.add_triangular('medium', FuzzyInputVariableTemperature_min, FuzzyInputVariableTemperature_middle, FuzzyInputVariableTemperature_max)
	temperature.add_triangular('hot', FuzzyInputVariableTemperature_middle, FuzzyInputVariableTemperature_max, FuzzyInputVariableTemperature_max)

	Soilhumidity = FuzzyInputVariable(FuzzyInputVariableSoilHumidity, FuzzyInputVariableSoilHumidity_min, FuzzyInputVariableSoilHumidity_max, 100)
	Soilhumidity.add_triangular('dry', FuzzyInputVariableSoilHumidity_min, FuzzyInputVariableSoilHumidity_min, FuzzyInputVariableSoilHumidity_required)
	Soilhumidity.add_triangular('medium', FuzzyInputVariableSoilHumidity_min, FuzzyInputVariableSoilHumidity_required, FuzzyInputVariableTemperature_max)
	Soilhumidity.add_triangular('wet', FuzzyInputVariableSoilHumidity_required, FuzzyInputVariableSoilHumidity_max, FuzzyInputVariableSoilHumidity_max)

	irrigation = FuzzyOutputVariable(FuzzyOutputVariableIrrigation, FuzzyOutputVariableIrrigation_min, FuzzyOutputVariableIrrigation_max, 100)
	irrigation.add_triangular('super slow', FuzzyOutputVariableIrrigation_min, FuzzyOutputVariableIrrigation_min, FuzzyOutputVariableIrrigation_min + irrigation_y - irrigation_x)
	irrigation.add_triangular('slow', FuzzyOutputVariableIrrigation_min, FuzzyOutputVariableIrrigation_min + irrigation_y - irrigation_x,   FuzzyOutputVariableIrrigation_min + (2*irrigation_y) - (2*irrigation_x))
	irrigation.add_triangular('normal', FuzzyOutputVariableIrrigation_min + irrigation_y - irrigation_x, FuzzyOutputVariableIrrigation_min + (2*irrigation_y) - (2*irrigation_x) , FuzzyOutputVariableIrrigation_max - irrigation_y + irrigation_x )
	irrigation.add_triangular('fast', FuzzyOutputVariableIrrigation_min + (2*irrigation_y) - (2*irrigation_x), FuzzyOutputVariableIrrigation_max - irrigation_y + irrigation_x, FuzzyOutputVariableIrrigation_max)
	irrigation.add_triangular('super fast', FuzzyOutputVariableIrrigation_max - irrigation_y + irrigation_x, FuzzyOutputVariableIrrigation_max, FuzzyOutputVariableIrrigation_max)


	system = FuzzySystem()
	system.add_input_variable(temperature)
	system.add_input_variable(Soilhumidity)
	system.add_output_variable(irrigation)

	# This rules does not contamplate if there is sun or not. They were created thinking that the irrigation is going to
	# happen only in dark hours.

	system.add_rule(
			{ 'Temperature':'cold',
				'Soil Humidity':'wet' },
			{ 'Water':'super slow'})

	system.add_rule(
			{ 'Temperature':'cold',
				'Soil Humidity':'medium' },
			{ 'Water':'normal'})

	system.add_rule(
			{ 'Temperature':'cold',
				'Soil Humidity':'dry' },
			{ 'Water':'fast'})

	system.add_rule(
			{ 'Temperature':'medium',
				'Soil Humidity':'wet' },
			{ 'Water':'super slow'})

	system.add_rule(
			{ 'Temperature':'medium',
				'Soil Humidity':'medium' },
			{ 'Water':'normal'})

	system.add_rule(
			{ 'Temperature':'medium',
				'Soil Humidity':'dry' },
			{ 'Water':'fast'})

	system.add_rule(
			{ 'Temperature':'hot',
				'Soil Humidity':'wet' },
			{ 'Water':'super slow'})

	system.add_rule(
			{ 'Temperature':'hot',
				'Soil Humidity':'medium' },
			{ 'Water':'fast'})

	system.add_rule(
			{ 'Temperature':'hot',
				'Soil Humidity':'dry' },
			{ 'Water':'super fast'})


	output = system.evaluate_output({
					'Temperature':5,
					'Soil Humidity':25
			})


	if (output['Water'] <= irrigationOffset): 
		print("El sistema de riego no se encederá, no se cumple con el offset definido por el usuario")

# si el sistema de riego se enciende que hago? 
# cuando termina tengo que guardar los datos en la base de datos 
#la humedad anterior primero, la hora de encendido tmb, y desp los otros datos los deberia guardar despues
# deberia tener un boolean que pregunte si esta encendido


	print(output)

