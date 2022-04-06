from django import forms
from .models import irrigationModel

class irrigationForm(forms.ModelForm):
    class Meta:
        model= irrigationModel
        fields= ["id","automatico", "encendido", "riego_diurno", "tiempo_maximo_riego",
                "envio_alertas", "cantidad_dias_sin_lluvia"]

