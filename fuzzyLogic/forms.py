from django import forms
from .models import irrigationHistoryModel

class irrigationHistoryForm(forms.ModelForm):
    class Meta:
        model= irrigationHistoryModel
        fields= ["duracion_maxima", "duracion", "cantidad_agua", "humedad_antes", "humedad_despues", "temperatura", "numero_paso"]
