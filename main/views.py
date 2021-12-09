from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

def home(request):
    return render(request, "home/home.html")

def get_data(request, *args, **kwargs):
    labels =  ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    default_items = [123, 2, 43, 532, 23, 2] 
    data = {
        "labels" : labels,
        "default": default_items,
    }
    return JsonResponse(data)


