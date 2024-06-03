from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.forms import ValidationError
from django.db.models import F, Q
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
token = os.environ.get('API_TOKEN')
web = "https://api.estadisticasbcra.com/"
headers = {"Authorization": token}

load_dotenv()
token = os.environ.get('API_TOKEN_2')


class Location(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    CODPROV = models.CharField(
        max_length=2, verbose_name='Código de Provincia')
    NOMPROV = models.CharField(
        max_length=20, verbose_name='Nombre de Provincia')
    CODDEPTO = models.CharField(
        max_length=3, verbose_name='Código de Departamento')
    NOMDEPTO = models.CharField(
        max_length=30, verbose_name='Nombre de Departamento')
    CODMUNI = models.CharField(
        max_length=4, verbose_name='Código de Municipio')
    NOMMUNI = models.CharField(
        max_length=30, verbose_name='Nombre de Municipio')
    CODLOC = models.CharField(
        max_length=3, verbose_name='Código de Localidad')
    CODAGLO = models.CharField(
        max_length=4, verbose_name='Código de Aglomerado')
    NOMLOC = models.CharField(
        max_length=30, verbose_name='Nombre de Localidad')

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        ordering = ['CODPROV', 'CODDEPTO', 'CODMUNI', 'CODLOC']

    def __str__(self):
        return self.NOMLOC


class Clases(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Clase')
    subname = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Subclase')

    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.subname}'


class Estados(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Estado')

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
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
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='Título')
    abreviation = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Abreviación')

    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'
        ordering = ['name']

    def __str__(self):
        return self.abreviation


class Empresas(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Nombres')
    propietario = models.CharField(
        max_length=200, verbose_name='Propietario', blank=True, null=True)
    representante_tecnico = models.CharField(
        max_length=200, verbose_name='Representante Técnico', blank=True, null=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name='Ubicación', blank=True, null=True)
    calle = models.CharField(
        max_length=200, verbose_name='Calle', blank=True, null=True)
    telephone = models.CharField(
        max_length=50, verbose_name='Teléfono', blank=True, null=True)
    email = models.EmailField(verbose_name='Correo', blank=True, null=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name


class Inspectores(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Nombres')
    surname = models.CharField(max_length=200, verbose_name='Apellidos')
    titulo = models.ForeignKey(
        Titulos, on_delete=models.CASCADE, verbose_name='Título')
    dni = models.CharField(max_length=8, verbose_name='DNI')
    telephone = models.CharField(max_length=50, verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Correo')
    fullname = models.CharField(
        max_length=200, editable=False, blank=True, null=True, verbose_name='Inspector')

    class Meta:
        verbose_name = 'Inspector'
        verbose_name_plural = 'Inspectores'
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Calcular la fecha de entrega
        self.fullname = f'{self.titulo.abreviation} {self.surname.upper()}, {self.name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname


class Uvis(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    fecha = models.DateField(verbose_name='Fecha', blank=True, null=True)
    valor = models.FloatField(verbose_name='Valor', blank=True, null=True)

    class Meta:
        verbose_name = 'Uvi'
        verbose_name_plural = 'Uvis'
        ordering = ['fecha']

    def __str__(self):
        return str(self.valor)


def UVI_BD(user_id, token):
    # endopint al que se llama (Ver listado de endpoins)
    endpoint = "uvi"
    # datos para el llamado
    url = f'{web}{endpoint}'
    # Llamado
    data_json = requests.get(url, headers=headers).json()
    # Armamos una tabla con los datos
    df = pd.DataFrame(data_json)
    df = df[df['d'] >= '2022-01-01']
    data_dict = df.to_dict(orient='records')
    # Actualizar la tabla Uvis
    for registro in data_dict:
        fecha = registro['d']
        valor = registro['v']
        # Buscar si el registro ya existe
        try:
            uvi_obj = Uvis.objects.get(fecha=fecha)
        except Uvis.DoesNotExist:
            # Crear un nuevo registro
            uvi_obj = Uvis(fecha=fecha, valor=valor)
        else:
            # Actualizar el valor del registro existente
            uvi_obj.valor = valor
        uvi_obj.save()


class EmpresaPoliza(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    empresa = models.CharField(
        max_length=50, verbose_name='Nombre de empresa aseguradora')
    location = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Domicilio')
    telefono = models.CharField(
        max_length=10, null=True, blank=True, verbose_name='Teléfono')
    creaEmpresa = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Empresa creada por', default=1)

    class Meta:
        verbose_name = 'Aseguradora'
        verbose_name_plural = 'Aseguradoras'
        ordering = ['empresa']

    def __str__(self):
        return self.empresa


class Obras(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    expedientes = models.CharField(max_length=30, verbose_name='Expediente')
    codObra = models.CharField(max_length=200, verbose_name='Cod. Obra', editable=False, blank=True, null=True)
    institucion = models.ForeignKey(Instituciones, on_delete=models.CASCADE, verbose_name='Institución')
    # inspector = models.ForeignKey(
    #     Inspectores, on_delete=models.CASCADE, verbose_name='Inspector')
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, verbose_name='Empresa', blank=True, null=True)
    inicio = models.DateField(verbose_name='Fecha de inicio')
    uvi = models.ForeignKey(Uvis, on_delete=models.CASCADE,verbose_name='Uvi', editable=False, blank=True, null=True)
    plazo = models.IntegerField(verbose_name='Plazo Contractual (días)')
    vencimiento_contractual = models.DateField(verbose_name='Vencimiento Contractual', blank=True, null=True)
    nombre_obra = models.CharField(max_length=250, verbose_name='Carátula Obra', null=True, blank=True)
    monto_contrato = models.FloatField(verbose_name='Monto de contrato ($)', blank=True, null=True)
    fecha_cotrato = models.DateField(verbose_name='Fecha de contrato', blank=True, null=True)
    monto_uvi = models.FloatField(verbose_name='Monto de contrato (UVIS)')
    valor_uvi_contrato = models.FloatField(verbose_name='Valor UVI contrato', blank=True, null=True)

    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
        ordering = ['institucion']

    def __str__(self):
        return f'{self.institucion.name} - {self.codObra}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the object first
        # Now self.id has a value
        self.codObra = f'{str(self.institucion.clase.subname)[:2].upper()}{str(self.id).zfill(4)}{str(self.institucion.location.NOMDEPTO)[:2].upper()}'
        self.vencimiento_contractual = self.inicio + timedelta(days=self.plazo)
        try:
            self.uvi = Uvis.objects.get(fecha=self.inicio)
        except Uvis.DoesNotExist:
            pass
        super().save(*args, **kwargs)  # Save the object again with the updated codObra


class Polizas(models.Model):
    codPol = models.CharField(
        max_length=200, verbose_name='Cod. Poliza', editable=False, unique=True, null=True)
    obra = models.ForeignKey(
        Obras, on_delete=models.CASCADE, verbose_name='Obra')
    tiene_poliza = models.BooleanField(
        null=True, blank=True, verbose_name='Presenta póliza de sustitución?')
    acta_fondo_reparo = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='Póliza de sustitución Fondo de Reparo')
    poliza_sustitucion = models.IntegerField(
        null=True, blank=True, verbose_name='N° Póliza Fondo de Reparo')
    empresa_poliza = models.ForeignKey(
        EmpresaPoliza, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Empresa aseguradora')
    monto_asegurado = models.FloatField(
        null=True, blank=True, verbose_name='Monto asegurado')
    orden = models.PositiveIntegerField(verbose_name='Nro Orden', default=1)
    obervacion = models.TextField(
        null=True, blank=True, verbose_name='Observación')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Creada por',)

    class Meta:
        verbose_name = 'Poliza'
        verbose_name_plural = 'Polizas'
        ordering = ['obra']

    def clean(self):
        if self.pk is None:
            pass

    def save(self, *args, **kwargs):
        self.codPol = f'{str(self.obra.codObra)}P{str(self.orden)}'
        if Polizas.objects.filter(codPol=self.codPol).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Esta obra ya cuenta con la poliza N° {self.orden}')
        super().save(*args, **kwargs)


class Rubros(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Rubro')

    class Meta:
        verbose_name = 'Rubro'
        verbose_name_plural = 'Rubros'
        ordering = ['name']

    def __str__(self):
        return self.name


class Unidades(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Unidad')

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['name']

    def __str__(self):
        return self.name


class Subrubros(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Item')
    rubro = models.ForeignKey(
        Rubros, on_delete=models.CASCADE, verbose_name='Rubro')
    unidad = models.ForeignKey(
        Unidades, on_delete=models.CASCADE, verbose_name='Unidad', blank=True, null=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['rubro', 'name']

    def __str__(self):
        return self.name


class Presupuestos(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    obra = models.ForeignKey(
        Obras, on_delete=models.CASCADE, verbose_name='Obra')
    fecha_presupuesto = models.DateField(
        verbose_name='Fecha Presupuesto', null=True)
    fecha_oferta = models.DateField(verbose_name='Fecha Oferta', null=True)
    uvi = models.ForeignKey(Uvis, on_delete=models.CASCADE,
                            verbose_name='Uvi', editable=False, blank=True, null=True)
    subrubro = models.ManyToManyField(
        Subrubros, through='PresupuestosSubrubros', blank=True, verbose_name='Items')

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['obra']

    def __str__(self):
        return f'{self.obra.codObra} - {self.obra.institucion.name}'

    def save(self, *args, **kwargs):
        self.uvi = Uvis.objects.get(fecha=self.fecha_oferta)
        super().save(*args, **kwargs)


class PresupuestosSubrubros(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    rubro_ok = models.BooleanField(default=False, verbose_name='Es Rubro?')
    nro_rubro = models.CharField(max_length=2, verbose_name='No. Rubro')
    nro_item = models.CharField(
        max_length=3, verbose_name='No. Item', blank=True, null=True)
    full_item = models.CharField(
        max_length=200, verbose_name='Item', editable=False)
    presupuesto = models.ForeignKey(
        Presupuestos, on_delete=models.CASCADE, verbose_name='Presupuesto', blank=True, null=True)
    rubro = models.ForeignKey(
        Rubros, on_delete=models.CASCADE, verbose_name='Rubro', blank=True, null=True)
    subrubro = models.ForeignKey(
        Subrubros, on_delete=models.CASCADE, verbose_name='Item', blank=True, null=True)
    unidad = models.ForeignKey(
        Unidades, on_delete=models.CASCADE, verbose_name='Unidad', blank=True, null=True)
    cantidad = models.FloatField(
        verbose_name='Cantidad', blank=True, null=True)
    # calculos auxiliares Presupuesto
    precio_unitario_presupuesto = models.FloatField(
        verbose_name='Precio Unit Presup', blank=True, null=True)
    precio_total_presupuesto = models.FloatField(
        verbose_name='Precio Total', editable=False, blank=True, null=True)
    incidencias_presupuesto = models.FloatField(
        verbose_name='Incidencias', editable=False, blank=True, null=True)
    # calculos auxiliares Oferta
    precio_unitario_oferta = models.FloatField(
        verbose_name='Precio Unit Oferta', blank=True, null=True)
    precio_total_oferta = models.FloatField(
        verbose_name='Precio Total', editable=False, blank=True, null=True)
    incidencias_oferta = models.FloatField(
        verbose_name='Incidencias', editable=False, blank=True, null=True)
    uvi_oferta = models.FloatField(
        verbose_name='Uvi', editable=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['presupuesto']

    def total_items_presupuesto(self):
        if self.rubro_ok == False:
            self.precio_total_presupuesto = self.cantidad * self.precio_unitario_presupuesto
        else:
            self.precio_total_presupuesto = None

    def total_items_oferta(self):
        if self.rubro_ok == False:
            self.precio_total_oferta = self.cantidad * self.precio_unitario_oferta
        else:
            self.precio_total_oferta = None

    def incidencia_presupuesto(self):
        presupuesto_id = PresupuestosSubrubros.objects.filter(
            presupuesto=self.presupuesto)
        if presupuesto_id.exists():
            total_presupuesto = presupuesto_id.aggregate(Sum('precio_total_presupuesto'))[
                'precio_total_presupuesto__sum']
            if self.precio_total_presupuesto:
                self.incidencias_presupuesto = round(
                    self.precio_total_presupuesto / total_presupuesto, 2)
            else:
                self.incidencias_presupuesto = None
        else:
            self.incidencias_presupuesto = None

    def incidencia_oferta(self):
        presupuesto_id = PresupuestosSubrubros.objects.filter(
            presupuesto=self.presupuesto)
        if presupuesto_id.exists():
            total_oferta = presupuesto_id.aggregate(Sum('precio_total_oferta'))[
                'precio_total_oferta__sum']
            if self.precio_total_oferta:
                self.incidencias_oferta = round(
                    self.precio_total_oferta / total_oferta, 2)
            else:
                self.incidencias_oferta = None
        else:
            self.incidencias_oferta = None

    def calculo_uvis(self):
        if PresupuestosSubrubros.objects.filter(presupuesto=self.presupuesto).exists():
            if self.incidencias_oferta:
                self.uvi_oferta = round(
                    self.incidencias_oferta * self.presupuesto.uvi.valor, 2)

    def save(self, *args, **kwargs):
        # PresupuestosSubrubros.objects.filter(presupuesto=self.presupuesto).exists()
        self.total_items_presupuesto()
        self.total_items_oferta()
        try:
            self.incidencia_presupuesto()
        except:
            print('error incidencia presupuesto')
        try:
            self.incidencia_oferta()
        except:
            print('error incidencia oferta')
        try:
            self.calculo_uvis()
        except:
            print('error calculo uvis')
        super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)


class Certificados(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    expediente = models.CharField(max_length=30, verbose_name='Expediente')
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    nro_cert = models.PositiveIntegerField(verbose_name='Certificado N°')
    codCert = models.CharField(max_length=200, verbose_name='Cod. Certificado', unique=True)
    fecha = models.DateField(verbose_name='Fecha del certificado')
    fecha_acta = models.DateField(verbose_name='Fecha que presenta Acta el Inspector', blank=True, null=True)
    uvi = models.FloatField(verbose_name='Cant UVIs certificados')
    uvi_acum = models.FloatField(verbose_name='Cant UVIs acumulados', default=0)
    avance_acum_proy = models.FloatField(verbose_name='Avance proyectado acumulado (%)', default=0)
    avance_acum_med = models.FloatField(verbose_name='Avance real acumulado (%)', default=0)
    coef_avance = models.BooleanField(verbose_name='Coef. Avance (%)', default=False)
    cargaCert = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    periodo = models.CharField(max_length=30, verbose_name='Periodo medido', null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora de creación')
    ultimo_editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados_modificados', null=True, blank=True, verbose_name='Último usuario editor')
    ultima_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha y hora de última modificación', blank=True, null=True)

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['obra', 'nro_cert']

    def clean(self):
        if self.pk is None:
            pass

    def validate_unique(self, exclude=None):
            if self.pk is None: 
                return
            try:
                certs = Certificados.objects.filter(codCert=self.codCert, obra=self.obra).exclude(pk=self.pk)
                if certs.exists():
                    raise ValidationError('Esta obra ya cuenta con certificado N° %s' % self.nro_cert)
            except:
                raise

    def save(self, *args, **kwargs):
        self.codCert = f'{str(self.obra.codObra)}C{str(self.nro_cert).zfill(2)}'
        try:
            anterior = Certificados.objects.filter(Q(obra=self.obra) & Q(nro_cert=self.nro_cert-1))
            self.uvi_acum = self.uvi + anterior.values('uvi_acum')[0]['uvi_acum']
        except:
            self.uvi_acum = self.uvi
        self.avance_acum_med = round((self.uvi_acum / self.obra.monto_uvi) * 100, 1)
        coef_avance = self.avance_acum_med / self.avance_acum_proy
        if coef_avance < 0.9:
            self.coef_avance = False
        else:
            self.coef_avance = True
        if self.fecha:
            self.periodo = str(self.fecha.strftime('%B %y')).title()
        try:
            ultimo = Certificados.objects.filter(obra=self.obra).order_by('-nro_cert').values('nro_cert')[0]['nro_cert']
        except:
            ultimo = 0
        if (self.nro_cert - ultimo > 1):
            raise ValidationError(
                f'El certificado N° {ultimo+1} se encuentra pendiente, verifique por favor!')
        try:
                certs = Certificados.objects.filter(codCert=self.codCert, obra=self.obra).exclude(pk=self.pk)
                if certs.exists():
                    raise ValidationError('Esta obra ya cuenta con certificado N° %s' % self.nro_cert)
        except:
            raise
        super().save(*args, **kwargs)


class ActaTipo(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Tipo de Acta')

    class Meta:
        verbose_name = 'Tipo de Acta'
        verbose_name_plural = 'Tipos de Actas'
        ordering = ['name']

    def __str__(self):
        return self.name


class ActasObras(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    obra = models.ForeignKey(
        Obras, on_delete=models.CASCADE, verbose_name='Obra')
    tipo = models.ForeignKey(
        ActaTipo, on_delete=models.CASCADE, verbose_name='Tipo de Acta')
    fecha = models.DateField(
        verbose_name='Fecha aplicación Acta', blank=True, null=True)
    orden = models.PositiveIntegerField(verbose_name='Nro Orden', default=1)
    dispo = models.CharField(
        max_length=200, verbose_name='Disposición', blank=True, null=True)
    codActa = models.CharField(
        max_length=200, verbose_name='Cod. Acta', editable=False, unique=True, null=True)

    class Meta:
        verbose_name = 'Acta obra'
        verbose_name_plural = 'Actas obras'
        ordering = ['obra']

    def clean(self):
        if self.pk is None:
            pass

    def save(self, *args, **kwargs):
        self.codActa = f'{str(self.obra.codObra)}A{str(self.tipo.id).zfill(2)}{str(self.orden).zfill(2)}'
        if ActasObras.objects.filter(codActa=self.codActa).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Esta obra ya cuenta con acta {self.tipo.name} N° {self.orden}')
        super().save(*args, **kwargs)


class Memorias(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    codMem = models.CharField(max_length=200, verbose_name='Cod. Memoria', editable=False, unique=True)
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    memoria = models.TextField(verbose_name='Memoria', blank=True, null=True)
    resumen = models.TextField(verbose_name='Resumen', blank=True, null=True)
    imagen = models.ImageField(upload_to='static/images', verbose_name='Imagen', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)

    class Meta:
        verbose_name = 'Memoria'
        verbose_name_plural = 'Memorias'
        ordering = ['obra']

    def clean(self):
        if self.pk is None:
            pass
    
    def __str__(self):
        return f'{self.obra.institucion} {self.obra.codObra}'
    def save(self, *args, **kwargs):
        self.codMem = f'{str(self.obra.codObra)}Mem'
        if self.memoria:
            genai.configure(api_key=token)
            model = genai.GenerativeModel(model_name="gemini-pro")

            consulta = f'''Objetivo: del texto: {self.memoria}, identificar los puntos clave para mejorando el argumento y redacción, ya que será la descripcion del artículo, y no debe superar los 2500 caracteres
            Introduccion:
            Contextualización del tema o ámbito en el que se enmarca la obra, presentación del problema principal que aborda la obra, importancia o relevancia del problema.
            Problematica:
            Descripción detallada del problema, incluyendo causas, consecuencias y posibles impactos. Análisis de las diferentes perspectivas o enfoques sobre el problema. Evidencia o datos que sustentan la problemática.
            Solucion planteada:
            Descripción detallada de la solución propuesta para acondicionar la obra, incluyendo fundamentos o argumentos que la sustentan, posibles beneficios o ventajas de la solución y recursos necesarios para su implementación.
            Resumen:
            Resumen de los puntos clave del informe. Reflexión sobre la viabilidad y potencial impacto de la solución propuesta. Aporte o valor de la obra para abordar el problema.'''
            response = model.generate_content(consulta)
            self.resumen = response.text.replace("**", "")
        else:
            self.resumen = ""
        if Memorias.objects.filter(codMem=self.codMem).exclude(pk=self.pk).exists():
            raise ValidationError('Esta obra ya cuenta con una memoria')
        super().save(*args, **kwargs)

class DispoInspector(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    dispo = models.CharField(max_length=30, verbose_name='Disposición')
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    inspector = models.ForeignKey(Inspectores, on_delete=models.CASCADE, verbose_name='Inspector')
    fecha = models.DateField(verbose_name='Fecha')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    observacion = models.TextField(verbose_name='Observación', blank=True, null=True)

    class Meta:
        verbose_name = 'Disp Inspector'
        verbose_name_plural = 'Disp Inspectores'
        ordering = ['inspector']
    def __str__(self):
        return f'{self.dispo} - {self.inspector}'
    def save(self, *args, **kwargs):
        self.dispo = self.dispo.upper()
        if DispoInspector.objects.filter(dispo=self.dispo).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe la %s' % self.dispo)
        super().save(*args, **kwargs)


