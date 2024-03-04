from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

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

class Titulos(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='Título')
    abreviation = models.CharField(max_length=10, blank=True, null=True, verbose_name='Abreviación')
    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'
        ordering = ['name']
    def __str__(self):
        return self.abreviation

class Inspectores(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Nombres')
    surname = models.CharField(max_length=200, verbose_name='Apellidos')
    titulo = models.ForeignKey(Titulos, on_delete=models.CASCADE, verbose_name='Título')
    dni = models.CharField(max_length=8, verbose_name='DNI')
    telephone = models.CharField(max_length=50, verbose_name='Teléfono')
    mail = models.EmailField(verbose_name='Correo')
    class Meta:
        verbose_name = 'Inspector'
        verbose_name_plural = 'Inspectores'
        ordering = ['name']
    def __str__(self):
        return f'{self.titulo.abreviation} {self.surname.upper()}, {self.name}'

class Obras(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    institucion = models.ForeignKey(Instituciones, on_delete=models.CASCADE, verbose_name='Institución')
    inspector = models.ForeignKey(Inspectores, on_delete=models.CASCADE, verbose_name='Inspector')
    inicio = models.DateField(verbose_name='Fecha de inicio')
    plazo = models.IntegerField(verbose_name='Plazo Contractual (días)')
    vencimiento_contractual = models.DateField(verbose_name='Vencimiento Contractual', editable=False)
    ampliacion_1 = models.IntegerField(verbose_name='1ra Ampliación (días)', blank=True, null=True)
    vencimiento_ampliacion_1 = models.DateField(verbose_name='Vencimiento 1ra Ampliación Contractual', editable=False, blank=True, null=True)
    ampliacion_2 = models.IntegerField(verbose_name='2da Ampliación (días)', blank=True, null=True)
    vencimiento_ampliacion_2 = models.DateField(verbose_name='Vencimiento 2da Ampliación Contractual', editable=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
        ordering = ['institucion']
    def __str__(self):
        return self.institucion.name

    def save(self, *args, **kwargs):
        # Calcular la fecha de entrega
        self.vencimiento_contractual = self.inicio + timedelta(days=self.plazo)
        if self.ampliacion_1:
            self.vencimiento_ampliacion_1 = self.inicio + timedelta(days=self.plazo) + timedelta(days=self.ampliacion_1)
        if self.ampliacion_2:
            self.vencimiento_ampliacion_2 = self.inicio + timedelta(days=self.plazo) + timedelta(days=self.ampliacion_1) + timedelta(days=self.ampliacion_2)
        
        super().save(*args, **kwargs)

