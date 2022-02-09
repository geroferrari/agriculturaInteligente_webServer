from django.db import models

class irrigationHistory(models.Model):
    fecha=models.DateTimeField(auto_now= True)
    duracion=models.SmallIntegerField()
    cantidad_agua=models.SmallIntegerField()
    humedad_antes=models.SmallIntegerField()
    humedad_despues=models.SmallIntegerField()

    class Meta:
        verbose_name='irrigationHistoryModel'
        verbose_name_plural='irrigationHistoryModels'
