from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

def home(request):
    return render(request, "home/home.html")

