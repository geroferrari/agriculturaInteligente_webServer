from django.db import models

class HistoricWeatherModel(models.Model):
    city = models.CharField(max_length=25)
    temperature = models.FloatField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    humidity= models.FloatField()
    precipitation = models.BooleanField()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'HistoricWeatherModel'

class FutureWeatherModel(models.Model):
    city = models.CharField(max_length=25)
    day = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity= models.FloatField()
    precipitation = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'FutureWeatherModel'