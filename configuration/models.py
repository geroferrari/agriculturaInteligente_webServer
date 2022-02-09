from django.db import models

# Create your models here.

class ConfigurationFieldModel(models.Model):
    nombre_campo=models.CharField(max_length=50)
    provincia=models.CharField(max_length=50)
    ciudad=models.CharField(max_length=50)
    temperatura_minima_local=models.SmallIntegerField()
    temperatura_maxima_local=models.SmallIntegerField()
    humedad_maxima_local=models.SmallIntegerField()
    humedad_minima_local=models.SmallIntegerField()
    humedad_requerida_local=models.SmallIntegerField()
    cultivo=models.CharField(max_length=50)
    cantidad_sensores=models.IntegerField()
    area_cubierta=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="ConfigurationFieldModel"

    def __str__(self):
        return self.nombre_campo


