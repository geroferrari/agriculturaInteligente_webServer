import threading
from time import sleep
from datetime import datetime
from .sensorsAPI import * 
from .models import *

class CreateMqttThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.started = datetime.now()

    def run(self):
        try:
            while True:
                mqttListener()
                sleep(3600)
        except Exception as e:
            print(e)


#https://github.com/pradeesi/Paho-MQTT-with-Python