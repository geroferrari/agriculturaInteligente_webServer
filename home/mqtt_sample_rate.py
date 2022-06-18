import json
import time
import platform
import paho.mqtt.client as mqtt
from django.core.mail import send_mail 

def sendConfirmEmail(email, data):
    mail_subject = 'Servidor - Cambio Tiempo Muestreo'
    message = f"Se cambió la cofiguración de un nodo, el estado actual es: {data} "
    print(message)
    to_email = email
    send_mail(mail_subject, message, 'gerooferrari@gmail.com', [to_email], fail_silently=False)

flag_connected = 0
remote_username = "AgriIntel"
remote_password = "Qwerty135"

sensorDataMQTTTopic = "intel_agri/sensor_data"

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print('connected (%s)' % client._client_id)

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0

def on_message(client, userdata, message):
    message = str(message.payload)
    if "," in message:
        [action, parameter] = message.split(",")
    else:
        action = message
        parameter = ""
    print(action)
    print(parameter)

client = mqtt.Client(client_id='RaspberryPi', clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.tls_set()  # <--- even without arguments
client.username_pw_set(username = remote_username, password = remote_password)
client.connect(host='b94fa7cf0c0f4fcd91c97460db5c0564.s2.eu.hivemq.cloud', port=8883)
client.loop_start()

########################################################################
#Main script
def send_sample_rate(data):

    sensorId = data["sensorId"]
    tiempoMuestreo = data["tiempoMuestreo"]

    serialString=f"Device Status: Sensor - Addr={sensorId}, Report_interval={tiempoMuestreo} "

    dataDictionary = {}
    dataDictionary["Address"] = sensorId
    dataDictionary["Humidity"] = 20
    dataDictionary["Report_interval"] = tiempoMuestreo
    dataDictionary["Battery"] = 100
    dataDictionary["RSSI"] = 0
    dataDictionary["Time"] = time.ctime(time.time())


    dataJSON = json.dumps(dataDictionary, indent = 4)

    sendConfirmEmail('gferrari@fi.uba.ar' , dataJSON)


    print(dataJSON)
    client.connect(host='b94fa7cf0c0f4fcd91c97460db5c0564.s2.eu.hivemq.cloud', port=8883)
    client.publish(sensorDataMQTTTopic, dataJSON, 2)
    print(dataJSON)


if __name__ == '__main__':
	send_sample_rate()


