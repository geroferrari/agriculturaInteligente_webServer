import threading

from .models import *

class SensorThread(threading.Thread):

    def __init__(self, total):
        self.total = total
        threading.Thread.__init__(self)

    def run(self):
        try:
            print("works")
        
        except:
            print("does not work")

#https://github.com/pradeesi/Paho-MQTT-with-Python
