from django.shortcuts import render
from django.db import *

def home(request):
    return render(request, "home/home.html")

