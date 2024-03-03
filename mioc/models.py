from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    CODPROV = models.CharField(max_length=2,verbose_name='Código de Provincia')
    NOMPROV = models.CharField(max_length=20,verbose_name='Nombre de Provincia')
    CODDEPTO = models.CharField(max_length=3,verbose_name='Código de Departamento')
    NOMDEPTO = models.CharField(max_length=30,verbose_name='Nombre de Departamento')
    CODMUNI = models.CharField(max_length=4,verbose_name='Código de Municipio')
    NOMMUNI = models.CharField(max_length=30,verbose_name='Nombre de Municipio')
    CODLOC = models.CharField(max_length=3,verbose_name='Código de Localidad')
    CODAGLO = models.CharField(max_length=4,verbose_name='Código de Aglomerado')
    NOMLOC = models.CharField(max_length=30,verbose_name='Nombre de Localidad')
    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        ordering = ['CODPROV', 'CODDEPTO', 'CODMUNI', 'CODLOC']
    def __str__(self):
        return self.NOMLOC

class Clases(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Clase')
    subname = models.CharField(max_length=200, blank=True, null=True, verbose_name='Subclase')
    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
        ordering = ['name']
    def __str__(self):
        return self.name

class Instituciones(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Institución')
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, verbose_name='Tipo de Institución')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Ubicación')
    geometry = models.CharField(max_length=150, blank=True, null=True, verbose_name='Georeferencia')
    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
        ordering = ['name']
    def __str__(self):
        return self.name


