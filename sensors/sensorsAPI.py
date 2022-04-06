import imp
import json
import time
import paho.mqtt.client
from django.db import connection


def on_connect(client, userdata, flags, rc):
	client.subscribe(topic='intel_agri/sensor_data/#', qos=2)

def checkTableExists(tablename):
	dbcur = connection.cursor()
	db_query = """SELECT name FROM sqlite_master WHERE type='table' AND name = '{tablename}' """
	listOfTables  = dbcur.execute(db_query).fetchall()
	dbcur.close()
	if listOfTables == []:
		print('Table not found!')
		return False
	else:
		print('Table found!')
		return True

def insertRowInTable(tablename, data):
	cursor = connection.cursor()
	database_row =""" INSERT INTO """ + tablename + """ (sensorId, humedad, bateria, tiempoMuestreo, estado, date) VALUES ('sensor0x00007' , '20' , '100' , '60' , 'conectado' , '2022-03-31 19:02:11.454627' ); """
	cursor.execute(database_row)


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


