from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.forms import ValidationError
from django.db.models import F, Q
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai
from dateutil.relativedelta import relativedelta

load_dotenv()
token = os.environ.get('API_TOKEN')
web = "https://api.estadisticasbcra.com/"
headers = {"Authorization": token}

load_dotenv()
token = os.environ.get('API_TOKEN_2')


class Location(models.Model):
    CODPROV = models.CharField(max_length=2, verbose_name='Código de Provincia')
    NOMPROV = models.CharField(max_length=20, verbose_name='Nombre de Provincia')
    CODDEPTO = models.CharField(max_length=3, verbose_name='Código de Departamento')
    NOMDEPTO = models.CharField(max_length=30, verbose_name='Nombre de Departamento')
    CODMUNI = models.CharField(max_length=4, verbose_name='Código de Municipio')
    NOMMUNI = models.CharField(max_length=30, verbose_name='Nombre de Municipio')
    CODLOC = models.CharField(max_length=3, verbose_name='Código de Localidad')
    CODAGLO = models.CharField(max_length=4, verbose_name='Código de Aglomerado')
    NOMLOC = models.CharField(max_length=30, verbose_name='Nombre de Localidad')

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
        return f'{self.name} - {self.subname}'


class Instituciones(models.Model):
    name = models.CharField(max_length=200, verbose_name='Institución')
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, verbose_name='Tipo de Institución')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Ubicación')
    domicilio = models.CharField(max_length=150, blank=True, null=True, verbose_name='Domicilio')
    frac = models.CharField(max_length=2, blank=True, null=True, verbose_name='Fracción')
    radio = models.CharField(max_length=2, blank=True, null=True, verbose_name='Radio')
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
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    cuit = models.CharField(max_length=11, verbose_name='CUIT', unique=True)
    name = models.CharField(max_length=200, verbose_name='Nombres')
    propietario = models.CharField(max_length=200, verbose_name='Propietario', blank=True, null=True)
    representante_tecnico = models.CharField(max_length=200, verbose_name='Representante Técnico', blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Ubicación', blank=True, null=True)
    calle = models.CharField(max_length=200, verbose_name='Calle', blank=True, null=True)
    telephone = models.CharField(max_length=50, verbose_name='Teléfono', blank=True, null=True)
    email = models.EmailField(verbose_name='Correo', blank=True, null=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name


class Inspectores(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Nombres')
    surname = models.CharField(max_length=200, verbose_name='Apellidos')
    titulo = models.ForeignKey(Titulos, on_delete=models.CASCADE, verbose_name='Título')
    dni = models.CharField(max_length=8, verbose_name='DNI', unique=True)
    telephone = models.CharField(max_length=50, verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Correo')
    fullname = models.CharField(max_length=200, editable=False, blank=True, null=True, verbose_name='Inspector')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario', blank=True, null=True)

    class Meta:
        verbose_name = 'Inspector'
        verbose_name_plural = 'Inspectores'
        ordering = ['fullname']

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
    cuit = models.CharField(max_length=11, verbose_name='CUIT')
    empresa = models.CharField(max_length=50, verbose_name='Nombre de empresa aseguradora')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='Domicilio')
    telefono = models.CharField(max_length=11, null=True, blank=True, verbose_name='Teléfono')
    creaEmpresa = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Empresa creada por', default=1)

    class Meta:
        verbose_name = 'Aseguradora'
        verbose_name_plural = 'Aseguradoras'
        ordering = ['empresa']

    def __str__(self):
        return self.empresa
    def save(self, *args, **kwargs):
        if EmpresaPoliza.objects.filter(cuit=self.cuit).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Ese CUIT ya esta registrado en otra aseguradora')
        super().save(*args, **kwargs)

class Obras(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    PLAZO_TIPO = (('0','Días'), ('1','Meses'), ('2','Años'))
    expedientes = models.CharField(max_length=30, verbose_name='Expediente', unique=True)
    dispo_contrato = models.CharField(max_length=30, verbose_name='Dispo. Contrato', unique=True)
    fecha_dispo = models.DateField(verbose_name='Fecha de dispo de Aceptación de Contrato')
    codObra = models.CharField(max_length=200, verbose_name='Cod. Obra', editable=False, blank=True, null=True)
    institucion = models.ForeignKey(Instituciones, on_delete=models.CASCADE, verbose_name='Institución')
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, verbose_name='Empresa')
    uvi = models.ForeignKey(Uvis, on_delete=models.CASCADE,verbose_name='Uvi', editable=False, blank=True, null=True)
    plazoTipo = models.CharField(max_length=1, verbose_name='Unidad de Tiempo', choices=PLAZO_TIPO, default='0')
    plazoNro = models.IntegerField(verbose_name='Plazo Contractual')
    nombre_obra = models.CharField(max_length=250, verbose_name='Carátula Obra')
    monto_contrato = models.FloatField(verbose_name='Monto de contrato ($)')
    fecha_cotrato = models.DateField(verbose_name='Fecha de contrato')
    monto_uvi = models.FloatField(verbose_name='Monto de contrato (UVIS)')
    valor_uvi_contrato = models.FloatField(verbose_name='Valor UVI a fecha de contrato')
    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
        ordering = ['institucion']
    def __str__(self):
        return f'{self.institucion.name} - {self.expedientes}'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.codObra = f'{str(self.institucion.clase.subname)[:2].upper()}{str(self.id).zfill(4)}{str(self.institucion.location.NOMDEPTO)[:2].upper()}'
        # try:
        #     self.uvi = Uvis.objects.get(fecha=self.inicio)
        # except Uvis.DoesNotExist:
        #     pass
        super().save(*args, **kwargs)


class Polizas(models.Model):
    codPol = models.CharField(max_length=200, verbose_name='Cod. Poliza', editable=False, unique=True, null=True)
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    tiene_poliza = models.BooleanField(null=True, verbose_name='Presenta póliza de sustitución?')
    acta_fondo_reparo = models.CharField(max_length=30, blank=True, null=True, verbose_name='Póliza de sustitución Fondo de Reparo')
    poliza_sustitucion = models.IntegerField(null=True, blank=True, verbose_name='N° Póliza Fondo de Reparo')
    empresa_poliza = models.ForeignKey(EmpresaPoliza, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Empresa aseguradora')
    monto_asegurado = models.FloatField(null=True, blank=True, verbose_name='Monto asegurado')
    orden = models.PositiveIntegerField(verbose_name='Nro Orden', default=1)
    obervacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creada por',)

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

class ActaMedicion(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    acta = models.PositiveIntegerField(verbose_name='N° Acta')
    periodo = models.DateField(verbose_name='Periodo de medición')
    registro = models.DateField(verbose_name='Fecha de registro', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    ultimo_editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actas_modificadas', null=True, blank=True, verbose_name='Último usuario editor')
    ultima_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha y hora de última modificación', blank=True, null=True)
    class Meta:
        verbose_name = 'Acta de Medición'
        verbose_name_plural = 'Actas de Medición'
    def __str__(self):
        return f'Acta {self.acta} - {self.obra.institucion.name}' 

    def validate_unique(self, exclude=None):
            if self.pk is None: 
                return
    def save(self, *args, **kwargs):
        try:
            ultimo = ActaMedicion.objects.filter(obra=self.obra).order_by('-acta').values('acta')[0]['acta']
        except:
            ultimo = 0
        if (self.acta - ultimo > 1):
            raise ValidationError(
                f'Acta N° {ultimo+1} se encuentra pendiente, corrija para continuar!')
        try:
            actaX = ActaMedicion.objects.filter(acta=self.acta, obra=self.obra).exclude(pk=self.pk)
            if actaX.exists():
                raise ValidationError('Esta obra ya cuenta con Acta N° %s' % self.acta)
        except:
            raise
        try:
            previous_acta = ActaMedicion.objects.filter(obra=self.obra).order_by('-periodo').values('periodo')[0]['periodo']
        except IndexError:  # Específicamente capturamos el error de índice
            previous_acta = '1900-01-01'
            previous_acta = datetime.strptime(previous_acta, '%Y-%m-%d').date()
        if (previous_acta.year, previous_acta.month) >= (self.periodo.year, self.periodo.month):
            raise ValidationError(f'Periodo de medioción esperado {previous_acta.month+1}/{previous_acta.year}, verifique para continuar!')
        
        super().save(*args, **kwargs)

class ActaMedicionValidacion(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    acta = models.ForeignKey(ActaMedicion, on_delete=models.CASCADE, verbose_name='Acta')
    validated = models.BooleanField(verbose_name='Validada para certificar',blank=True, null=True)
    observacion = models.TextField(max_length=1000, verbose_name='Observación', blank=True, null=True)
    registro = models.DateField(verbose_name='Fecha de registro', auto_now_add=True)
    
    uvi = models.FloatField(verbose_name='UVIs del Certificado')
    uvi_acum = models.FloatField(verbose_name='Cant UVIs acumulados', default=0)
    avance_acum_proy = models.FloatField(verbose_name='Avance proyectado acumulado (%)', default=0)
    avance_acum_med = models.FloatField(verbose_name='Avance real acumulado (%)', default=0)
    coef_avance = models.BooleanField(verbose_name='Coef. Avance (%)', default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    ultimo_editor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='validaciones_modificadas' ,null=True, blank=True, verbose_name='Último usuario editor')
    ultima_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha y hora de última modificación', blank=True, null=True)
    class Meta:
        verbose_name = 'Acta de Validación'
        verbose_name_plural = 'Actas de Validación'
    def __str__(self):
        return f'Acta de Validación {self.acta.acta}@{self.acta.obra.institucion.name}'
    def save(self, *args, **kwargs):
        if ActaMedicionValidacion.objects.filter(acta=self.acta).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe una validación para esta acta')
        try:
            anterior = ActaMedicionValidacion.objects.filter(Q(acta__obra=self.acta.obra) & Q(acta__acta=self.acta.acta-1))
            self.uvi_acum = self.uvi + anterior.values('uvi_acum')[0]['uvi_acum']
        except:
            self.uvi_acum = self.uvi
        
        self.avance_acum_med = round((self.uvi_acum / self.acta.obra.monto_uvi) * 100, 1)
        if self.avance_acum_med > 100:
            raise ValidationError(f'Esta superando el monto contratado por un {round(self.avance_acum_med-100,2)}% de más, corrija para continuar!')
        coef_avance = self.avance_acum_med / self.avance_acum_proy
        if coef_avance < 0.9:
            self.coef_avance = False
        else:
            self.coef_avance = True

        super().save(*args, **kwargs)

    
class Certificados(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    acta = models.ForeignKey(ActaMedicion, on_delete=models.CASCADE, verbose_name='Acta de Medición')
    expediente = models.CharField(max_length=30, verbose_name='Expediente')
    cargaCert = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora de creación')
    ultimo_editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados_modificados', null=True, blank=True, verbose_name='Último usuario editor')
    ultima_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha y hora de última modificación', blank=True, null=True)
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['acta__obra', 'acta__acta']

    def save(self, *args, **kwargs):
        if Certificados.objects.filter(expediente=self.expediente).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe el expediente indicado en otro certificado')
        super().save(*args, **kwargs)

class dispo_plan_trabajo(models.Model):
    opciones = (('0', 'Plan de Trabajo Original'), ('1', 'Nuevo Plan de Trabajo'))
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    instrumento = models.CharField(max_length=30, verbose_name='Instrumento en GDE')
    fecha_aplicacion = models.DateField(verbose_name='Fecha de aplicación')
    tipo = models.CharField(max_length=1, choices=opciones, verbose_name='Tipo', default='0')
    nro_plan = models.PositiveIntegerField(verbose_name='Nro. Plan', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creado por', default=1)
    class Meta:
        verbose_name = 'Dispo. Plan de Trabajo'
        verbose_name_plural = 'Dispos. Plan de Trabajo'
        ordering = ['obra']
    def __str__(self):
        return f'Plan {str(self.nro_plan).zfill(2)} - {str(self.fecha_aplicacion.day).zfill(2)}/{str(self.fecha_aplicacion.month).zfill(2)}/{str(self.fecha_aplicacion.year)} - {self.obra.institucion}'
    def save(self, *args, **kwargs):
        if (self.tipo)=='0':
            self.nro_plan = 1
        elif dispo_plan_trabajo.objects.filter(Q(obra__codObra=self.obra.codObra) & Q(tipo='0')).order_by('nro_plan').exists():
            ultimo = dispo_plan_trabajo.objects.filter(obra__codObra=self.obra.codObra).order_by('nro_plan').values('nro_plan').last()
            self.nro_plan = ultimo['nro_plan'] + 1
        else:
            raise ValidationError(f'La obra aún no cuenta con un plan de trabajo Inicial')
        if dispo_plan_trabajo.objects.filter(Q(obra__codObra=self.obra.codObra) & Q(nro_plan=self.nro_plan)).exclude(pk=self.pk).exists():
            raise ValidationError(f'Esta obra ya cuenta con un Plan de Trabajo Original, quizas sea un "Nuevo Plan de Trabajo"?')
        if dispo_plan_trabajo.objects.filter(instrumento=self.instrumento).exclude(pk=self.pk).exists():
            raise ValidationError(f'Ya existe un plan de trabajo con el instrumento {self.instrumento}')
        if (self.obra.fecha_dispo) > (self.fecha_aplicacion):
            raise ValidationError(f'Revise la fecha de implementación del Plan de Trabajo, ya que no puede ser anterior a la dispo de Aceptación de contrato {self.obra.fecha_dispo.day}/{self.obra.fecha_dispo.month}/{self.obra.fecha_dispo.year}')
        try:
            ultimo_certificado = Certificados.objects.filter(acta__obra__codObra=self.obra.codObra).order_by('id').values('acta__periodo').last()['acta__periodo']
        except:
            ultimo_certificado = self.obra.fecha_dispo
        if (ultimo_certificado) > (self.fecha_aplicacion):
            raise ValidationError(f'Revise la fecha de implementación del Plan de Trabajo, ya que hay certificados con fecha posterior a esta fecha')
        super().save(*args, **kwargs)

class PlanTrabajo(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    dispo_plan = models.ForeignKey(dispo_plan_trabajo, on_delete=models.CASCADE, verbose_name='Dispo. Plan de Trabajo')
    periodoNro = models.PositiveIntegerField(verbose_name='Periodo N°')
    fechaPeriodo = models.DateField(verbose_name='Fecha del Periodo')
    uvisEsperados = models.FloatField(verbose_name='UVIS Esperados')
    uvisAcumEsperados = models.FloatField(verbose_name='UVIS Acum. Esperados',default=0)
    ultimo = models.BooleanField(verbose_name='Ultimo Periodo', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creado por', default=1)
    class Meta:
        verbose_name = 'Plan de Trabajo'
        verbose_name_plural = 'Planes de Trabajo'
        ordering = ['dispo_plan','periodoNro']
    def __str__(self):
        return f'{self.dispo_plan.obra.codObra} - {self.dispo_plan.instrumento} - {self.dispo_plan.nro_plan} - {self.periodoNro}'
    def save(self, *args, **kwargs):
        try:
            ultimo_periodo = PlanTrabajo.objects.filter(dispo_plan=self.dispo_plan).order_by('periodoNro').values('periodoNro').last()['periodoNro']
        except:
            ultimo_periodo = 0
            self.periodoNro = 1
        if (self.periodoNro - ultimo_periodo > 1):
            raise ValidationError(
                f'Revise el nro. de Periodo, ya que esta pendiente el periodo N° {ultimo_periodo + 1}')
        try:
            NroX = PlanTrabajo.objects.filter(periodoNro=self.periodoNro, dispo_plan=self.dispo_plan).exclude(pk=self.pk)
            if NroX.exists():
                raise ValidationError('Esta obra ya cuenta con ese Periodo')
        except:
            raise
        try:
            anterior = PlanTrabajo.objects.filter(Q(dispo_plan=self.dispo_plan) & Q(periodoNro=self.periodoNro-1))
            self.uvisAcumEsperados = self.uvisEsperados + anterior.values('uvisAcumEsperados').last()['uvisAcumEsperados']
        except:
            self.uvisAcumEsperados = self.uvisEsperados
        if (self.uvisAcumEsperados - self.uvisEsperados) == (self.dispo_plan.obra.monto_uvi):
            raise ValidationError(f'Ya no hay periodos a proyectar, ya que se completo el Plan de Trabajo')
        elif (self.uvisAcumEsperados) > (self.dispo_plan.obra.monto_uvi):
            dife = round((self.dispo_plan.obra.monto_uvi) - (self.uvisAcumEsperados - self.uvisEsperados),2)
            raise ValidationError(f'Revise los UVIS esperados, ya que restan {dife} UVIS para concluir el contrato')
        if (self.uvisAcumEsperados) == (self.dispo_plan.obra.monto_uvi):
            PlanTrabajo.objects.filter(dispo_plan=self.dispo_plan).update(ultimo=True)
            self.ultimo = True
        else:
            PlanTrabajo.objects.filter(dispo_plan=self.dispo_plan).update(ultimo=False)
            self.ultimo = False
        super().save(*args, **kwargs)

class ActasInicio(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    fecha = models.DateField(verbose_name='Fecha de inicio')
    vencimiento_contractual = models.DateField(verbose_name='Vencimiento Contractual',editable=False,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)

    class Meta:
        verbose_name = 'Acta de inicio'
        verbose_name_plural = 'Actas de inicio'
        ordering = ['obra']
    def save(self, *args, **kwargs):
        if ActasInicio.objects.filter(obra__codObra=self.obra.codObra).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Esta obra ya cuenta con acta de inicio')
        try:
            fecha_dispo_insp = DispoInspector.objects.filter(obra=self.obra).order_by('fecha').values('fecha')[0]['fecha']
        except IndexError:
            fecha_dispo_insp = '1900-01-01'
            fecha_dispo_insp = datetime.strptime(fecha_dispo_insp, '%Y-%m-%d').date()
        if (fecha_dispo_insp) > (self.fecha):
            raise ValidationError(f'El acta de inicio debe ser igual o posterior a la disposición de inspector: {str(fecha_dispo_insp.day).zfill(2)}/{str(fecha_dispo_insp.month).zfill(2)}/{fecha_dispo_insp.year}')
        fecha_dispo_contrato = Obras.objects.filter(codObra=self.obra.codObra).order_by('id').values('fecha_dispo')[0]['fecha_dispo']
        if (fecha_dispo_contrato + timedelta(days=30))  < (self.fecha):
            raise ValidationError(f'La fecha de inicio, no puede superar los 30 dias desde la disposición de aprobacion del contrato')
        if (self.obra.plazoTipo) == '0':
            self.vencimiento_contractual = self.fecha + timedelta(days=self.obra.plazoNro)
        elif (self.obra.plazoTipo) == '1':
            self.vencimiento_contractual = self.fecha + relativedelta(months=self.obra.plazoNro)
        else:
            self.vencimiento_contractual = self.fecha + relativedelta(years=self.obra.plazoNro)
        super().save(*args, **kwargs)

class DispoParalizacion(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    dispo = models.CharField(max_length=30, verbose_name='Disposición de paralización')
    dispo_plan = models.ForeignKey(dispo_plan_trabajo, on_delete=models.CASCADE, verbose_name='Disposición de Plan de Trabajo')
    fecha_paralizacion = models.DateField(verbose_name='Fecha de paralización')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)

    class Meta:
        verbose_name = 'Disposición de paralización'
        verbose_name_plural = 'Disposiciones de paralización'
        ordering = ['dispo_plan','fecha_paralizacion']
    def save(self, *args, **kwargs):
        if DispoParalizacion.objects.filter(dispo_plan__obra=self.dispo_plan.obra).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Esta obra ya cuenta con disposición de paralización')
        super().save(*args, **kwargs)
    def __str__(self):
        return f'P{self.dispo_plan.nro_plan}@{self.dispo_plan.instrumento} {self.dispo_plan.obra.institucion}'

class DispoReinicio(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    dispo = models.CharField(max_length=30, verbose_name='Disposición de reinicio')
    dispo_para = models.ForeignKey(DispoParalizacion, on_delete=models.CASCADE, verbose_name='Disposición de Paralización')
    fecha_reinicio = models.DateField(verbose_name='Fecha de reinicio')
    dias_pend = models.IntegerField(verbose_name='Días pendientes', default=0)
    dias_pend_acum = models.IntegerField(verbose_name='Días pendientes acumulados', default=0)
    nuevo_vencimiento = models.DateField(verbose_name='Nueva Fecha de Vencimiento Contractual', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)

    class Meta:
        verbose_name = 'Disposición de reinicio'
        verbose_name_plural = 'Disposiciones de reinicio'
        ordering = ['dispo_para','fecha_reinicio']
    def save(self, *args, **kwargs):
        if DispoReinicio.objects.filter(dispo_para=self.dispo_para).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Esta obra ya cuenta con disposición de reinicio')
        self.dias_pend = (self.fecha_reinicio - self.dispo_para.fecha_paralizacion).days
        try:
            dias_pend_acum = DispoReinicio.objects.filter(dispo_para=self.dispo_para).order_by('fecha_reinicio').values('dias_pend').last()['dias_pend']
            self.dias_pend_acum = dias_pend_acum + self.dias_pend
        except:
            self.dias_pend_acum = self.dias_pend
        self.nuevo_vencimiento = ActasInicio.objects.filter(obra=self.dispo_para.dispo_plan.obra).order_by('id').values('vencimiento_contractual')[0]['vencimiento_contractual'] + timedelta(days=self.dias_pend_acum)
        super().save(*args, **kwargs)
    def __str__(self):
        return f'R{self.dispo_para.dispo_plan.nro_plan}@{self.dispo_para.dispo_plan.instrumento} {self.dispo_para.dispo_plan.obra.institucion}'

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
            Conclusión:
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

class AnticipoFinanciero(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    anticipo = models.BooleanField(verbose_name='Anticipo', null=True,default=False)
    dispo = models.CharField(max_length=30, verbose_name='Disposición', null=True, blank=True)
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    porcentaje = models.FloatField(verbose_name='Porcentaje',null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)

    class Meta:
        verbose_name = 'Anticipo financiero'
        verbose_name_plural = 'Anticipos financieros'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.obra.institucion} {self.obra.expedientes}'
    def save(self, *args, **kwargs):
        if AnticipoFinanciero.objects.filter(obra__codObra=self.obra.codObra).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe un anticipo financiero para esta obra')
        fecha_inicio = ActasInicio.objects.filter(obra__codObra=self.obra.codObra).order_by('fecha').values('fecha')[0]['fecha']
        if self.fecha==None:
            fecha_AF = fecha_inicio
        else:
            fecha_AF = self.fecha
        if (fecha_inicio) > (fecha_AF):
            raise ValidationError('La fecha del anticipo financiero, no puede ser anterior a la de inicio de obra')
        super().save(*args, **kwargs)

class CertificadosAF(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    dispo = models.ForeignKey(AnticipoFinanciero, on_delete=models.CASCADE, verbose_name='Obra')
    expediente = models.CharField(max_length=30, verbose_name='Expediente del certificado AF')
    monto = models.FloatField(verbose_name='Monto del Certificado')
    uvi = models.FloatField(verbose_name='UVIs')
    fecha = models.DateField(verbose_name='Fecha')
    cargaCert = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora de creación')
    # ultimo_editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados_modificados', null=True, blank=True, verbose_name='Último usuario editor')
    ultima_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha y hora de última modificación', blank=True, null=True)
    class Meta:
        verbose_name = 'Certificado AF'
        verbose_name_plural = 'Certificados Af'
        ordering = ['-fecha']
    def save(self, *args, **kwargs):
        if CertificadosAF.objects.filter(expediente=self.expediente).exclude(pk=self.pk).exists():
            raise ValidationError(f'Ya existe un expte {self.expediente}, revise para continuar')
        self.monto = round(self.dispo.porcentaje/100 * self.dispo.obra.monto_contrato,2)
        self.uvi = round(self.dispo.porcentaje/100 * self.dispo.obra.monto_uvi,2)
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.dispo.obra.institucion}, {self.expediente}'

class dispoCertAF(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    certificado = models.ForeignKey(CertificadosAF, on_delete=models.CASCADE, verbose_name='Certificado')
    dispo = models.CharField(max_length=30, verbose_name='Disposición Aprueba Certificado AF')
    fecha = models.DateField(verbose_name='Fecha Dispo')
    cargaCert = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora de creación')
    observacion = models.TextField(verbose_name='Observación', null=True, blank=True)
    class Meta:
        verbose_name = 'Disposición Certificado AF'
        verbose_name_plural = 'Disposiciones Certificados AF'
        ordering = ['-fecha']
    def save(self, *args, **kwargs):
        if dispoCertAF.objects.filter(dispo=self.dispo).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe la %s' % self.dispo)
        super().save(*args, **kwargs)

class Estructuras(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, verbose_name='Obra')
    link = models.URLField(verbose_name='Link', null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha', null=True, blank=True)
    inspector = models.ForeignKey(Inspectores, on_delete=models.CASCADE, verbose_name='Inspector',editable=False ,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    class Meta:
        verbose_name = 'Estructura'
        verbose_name_plural = 'Estructuras'
        ordering = ['obra']
    def __str__(self):
        return f'{self.obra.institucion} {self.obra.codObra}'
    def save(self, *args, **kwargs):
        if Estructuras.objects.filter(obra__codObra=self.obra.codObra).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe una estructura para esta obra')
        insp_asignado = DispoInspector.objects.filter(obra__codObra=self.obra.codObra).order_by('-fecha').first()
        if insp_asignado:
            self.inspector = insp_asignado.inspector  # Assign the actual Inspectores instance
        super().save(*args, **kwargs)

class facturasAF(models.Model):
    tipoF = (('0','A'),('1','B'),('2','C'))
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    certificado = models.ForeignKey(CertificadosAF, on_delete=models.CASCADE, verbose_name='Certificado')
    tipo = models.CharField(max_length=1, verbose_name='Tipo', choices=tipoF, default='1')
    pto_venta = models.PositiveIntegerField(verbose_name='Punto de Venta N°')
    comprobante = models.PositiveIntegerField(verbose_name='Comprobante N°')
    fecha = models.DateField(verbose_name='Fecha Emisión')
    cuit = models.CharField(max_length=11, verbose_name='CUIT Empresa')
    monto = models.FloatField(verbose_name='Importe Total')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cargado por', default=1)
    class Meta:
        verbose_name = 'Factura Certificado AF'
        verbose_name_plural = 'Facturas Certificados AF'
        ordering = ['-fecha']
    def __str__(self):
        return f'{self.cuit} {self.pto_venta}-{self.comprobante}'
    def save(self, *args, **kwargs):
        obra = CertificadosAF.objects.filter(dispo=self.certificado.dispo)
        cuit = obra.first().dispo.obra.empresa.cuit
        monto = obra.first().monto
        fecha = obra.first().dispo.fecha
        if not cuit == self.cuit:
            raise ValidationError(f'No coincide el CUIT de la empresa ({cuit}), con el CUIT de la Factura ({self.cuit})')
        if not monto == self.monto:
            raise ValidationError(f'No coincide el Monto de la Factura (${self.monto}), con el Monto de la Dispo (${monto})')
        if not fecha <= self.fecha:
            raise ValidationError(f'La Fecha de Emisión de la Factura ({self.fecha.day}/{self.fecha.month}/{self.fecha.year}), no puede ser anterior a la Fecha de Emisión de la Dispo ({fecha.day}/{fecha.month}/{fecha.year})')
        super().save(*args, **kwargs)