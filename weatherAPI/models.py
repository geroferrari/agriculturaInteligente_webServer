from django.db import models

class HistoricWeatherModel(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    precipitation = models.BooleanField()
    precipitation_prob = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'HistoricWeatherModel'
