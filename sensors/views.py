from django.shortcuts import render

def sensors(request):
    return render(request, "sensors/sensors.html", {"posts": posts})