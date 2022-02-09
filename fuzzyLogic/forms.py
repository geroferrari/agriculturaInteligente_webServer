from django import forms
from .models import irrigationHistory

class irrigationHistoryForm(forms.ModelForm):
    class Meta:
        model= irrigationHistory
        fields= ["duracion", "cantidad_agua", "humedad_antes", "humedad_despues"]

