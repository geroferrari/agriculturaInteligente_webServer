from django.shortcuts import render, redirect
from .forms import ConfigurationFieldForm

def configuration_field(request):
    ConfigurationFieldValues=ConfigurationFieldForm()

    if request.method == "POST":
        ConfigurationFieldValues=ConfigurationFieldForm(data=request.POST)
        ConfigurationFieldValues.save()
    # falta hacer una corroboracion/validacion de los datos    
    return render(request, "configuration/configuration_field.html", {'ConfigurationFieldValues': ConfigurationFieldValues})
