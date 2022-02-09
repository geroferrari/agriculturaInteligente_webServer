import threading
from time import sleep
from weatherAPI.views import weatherAPIData
from datetime import datetime


class CreateWeatherAPIThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.started = datetime.now()

    def run(self):
        try:
            i=1
            while (i == 1):
                weatherAPIData()    
                sleep(3600)
            
        except Exception as e:
            print(e)
