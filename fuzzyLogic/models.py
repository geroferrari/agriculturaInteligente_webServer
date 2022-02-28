from django.db import models

class irrigationHistoryModel(models.Model):
    fecha=models.DateTimeField(auto_now_add=True)
    duracion_maxima=models.SmallIntegerField()
    duracion=models.SmallIntegerField()
    cantidad_agua=models.SmallIntegerField()
    humedad_antes=models.SmallIntegerField()
    humedad_despues=models.SmallIntegerField()
    temperatura=models.SmallIntegerField()
    numero_paso=models.SmallIntegerField()

    class Meta:
        verbose_name='irrigationHistoryModel'
        verbose_name_plural='irrigationHistoryModels'
