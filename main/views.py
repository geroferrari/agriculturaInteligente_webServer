from django.shortcuts import render
from fuzzyLogic.thread import CreateFuzzyThread
from weatherAPI.thread import CreateWeatherAPIThread

def home(request):
    CreateFuzzyThread().start()
    CreateWeatherAPIThread().start()
    return render(request, "home/home.html")
