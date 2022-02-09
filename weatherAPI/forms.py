from django.forms import ModelForm, TextInput
from .models import HistoricWeatherModel 

class HistoricWeatherForm(ModelForm):
    class Meta:
        model = HistoricWeatherModel 
        fields = ['date',  'temperature', 'temperature_min', 'temperature_max', 'precipitation', 'precipitation_prob' ]

