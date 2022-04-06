from django import forms
from .models import ConfigurationFieldModel

class ConfigurationFieldForm(forms.ModelForm):
    class Meta:
        model= ConfigurationFieldModel
        fields= ["id", "nombre_campo", "provincia", "ciudad", "humedad_maxima_local", "humedad_minima_local",
                 "humedad_requerida_local", "cultivo", "area_cubierta"]

