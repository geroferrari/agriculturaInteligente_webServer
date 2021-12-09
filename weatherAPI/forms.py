from django.forms import ModelForm, TextInput
from .models import HistoricWeatherModel, FutureWeatherModel 

class HistoricWeatherForm(ModelForm):
    class Meta:
        model = HistoricWeatherModel 
        fields = ['city',  'temperature', 'temperature_min', 'temperature_max', 'humidity', 'precipitation' ]
        widgets = {'city' : TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}

class FutureWeatherForm(ModelForm):
    class Meta:
        model = FutureWeatherModel 
        fields = ['city', 'temperature', 'humidity', 'precipitation'  ]
        widgets = {'city' : TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}        