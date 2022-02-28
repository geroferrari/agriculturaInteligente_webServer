import imp
import time
import paho.mqtt.client
from django.db import connection


def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='sensors_data/', qos=2)

def on_message(client, userdata, message):
    # recibir mensaje
    # guardarlo
    # identificar a que sensor corresponde cada uno
    # asociarlo con la base de dato correspondiente
    #guardar datos
    print(message.payload)

def mqttListener():
	client = paho.mqtt.client.Client(client_id='server', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_start()

if __name__ == '__mqttListener__':
	mqttListener()
