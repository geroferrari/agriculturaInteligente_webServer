from django.db import models

class irrigationModel(models.Model):
    automatico=models.CharField(max_length=4)
    encendido=models.CharField(max_length=4)
    riego_diurno=models.CharField(max_length=4)
    tiempo_maximo_riego=models.SmallIntegerField()
    envio_alertas=models.CharField(max_length=4)
    cantidad_dias_sin_lluvia=models.SmallIntegerField()

    class Meta:
        verbose_name='irrigationModel'
        verbose_name_plural='irrigationModels'

