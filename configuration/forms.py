from django import forms
from .models import ConfigurationFieldModel

class ConfigurationFieldForm(forms.ModelForm):
    class Meta:
        model= ConfigurationFieldModel
        fields= ["nombre_campo", "provincia", "ciudad", "temperatura_minima_local", 
                "temperatura_maxima_local", "humedad_maxima_local", "humedad_minima_local",
                 "humedad_requerida_local", "cultivo",  "cantidad_sensores", "area_cubierta"]

