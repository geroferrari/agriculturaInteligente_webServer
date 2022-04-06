import time
import platform
from Receive_from_CC1352R import receiveData
import paho.mqtt.client as mqtt

flag_connected = 0
remote_username = "AgriIntel"
remote_password = "Qwerty135"
data = receiveData()

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
def main():

    serialString = ""  # Used to hold data coming over UART
    while 1:

        # Wait until there is data waiting in the serial buffer
        while True:

            serialString="Device Status: Sensor - Addr=0x00008, Temp=25,Humidity=2082, Battery=100, RSSI=67 Time=2022/03/22-08:42:11"
            try:
                #Get the data from the sensors, if there is any
                sensorsData = data.processReading(serialString)

                #Send data to Mosquitto
                for sensorData in sensorsData:   
                    if flag_connected == 0:
                      client.connect(host='b94fa7cf0c0f4fcd91c97460db5c0564.s2.eu.hivemq.cloud', port=8883)
                    client.publish(sensorDataMQTTTopic, sensorData, 2)
                    time.sleep(60)
                    print(sensorData)

                serialString = ""
            
            except:
                serialString = ""

if __name__ == '__main__':
	main()

