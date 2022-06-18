import imp
import json
import time
import paho.mqtt.client
from django.db import connection
from configuration.models import ConfigurationFieldModel


def on_connect(client, userdata, flags, rc):
	client.subscribe(topic='intel_agri/sensor_data/#', qos=2)

def checkTableExists(tablename):
	dbcur = connection.cursor()
	db_query = " SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + tablename + "' " 
	dbcur.execute(db_query)
	print(db_query)
	if dbcur.fetchone()[0]==1:
		print('Table found!')
		dbcur.close()
		return True
	else:
		print('Table not found!')
		sensores = ConfigurationFieldModel.objects.first()
		sensores.cantidad_sensores +=1
		sensores.save()
		dbcur.close()
		return False

def insertRowInTable(tablename, data):
	cursor = connection.cursor()
	database_row =""" INSERT INTO """ + tablename + """ (sensorId, humedad, bateria, tiempoMuestreo, estado, date) VALUES ( %s ,  %s , %s ,  %s , %s ,  %s ); """
	db_values =(data['Address'], data['Humidity'], data['Battery'], data['Report_interval'], 'conectado', data['Time'])
	cursor.execute(database_row, db_values)


def on_message(client, userdata, message):
	print("message received")
	m_decode = message.payload.decode("utf-8", "ignore")
	json_message = json.loads(m_decode)
	print(json_message)
	sensorId = "sensor" + json_message["Address"]
	print(sensorId)

	if checkTableExists(sensorId) == False:
		cursor = connection.cursor()
		print ("creating table..")
		database_name = "CREATE TABLE IF NOT EXISTS " + sensorId + " ('id' integer NOT NULL PRIMARY KEY AUTOINCREMENT, 'sensorId' varchar(10), 'humedad' smallint, 'bateria' smallint, 'tiempoMuestreo' smallint, 'estado' bool, 'date' datetime )"
		cursor.execute(database_name)
		cursor.close()
	
	insertRowInTable(sensorId, json_message)   

def mqttListener():
	print("Thread started")
	client = paho.mqtt.client.Client(client_id='server', clean_session=False)
	client.tls_set(tls_version=paho.mqtt.client.ssl.PROTOCOL_TLS)
	client.username_pw_set("AgriIntel", "Qwerty135")
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='b94fa7cf0c0f4fcd91c97460db5c0564.s2.eu.hivemq.cloud', port=8883)
	client.loop_start()


