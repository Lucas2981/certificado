from django.forms import DateInput, ModelForm
from .models import ActasObras, DispoInspector, Memorias, Obras, EmpresaPoliza, Certificados, Polizas, Instituciones
from django import forms
# llamar librerias de admin para autocompletar
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin


class ObraFormAll(ModelForm):
    class Meta:
        model = Obras
        fields = '__all__'
        # widgets = {
        #     'institucion': AutocompleteSelect(
        #         Obras._meta.get_field('institucion').remote_field,
        #         admin.site,
        #     )
        # }


class ObraFormActas(ModelForm):
    class Meta:
        model = Obras
        fields = ['monto_contrato', 'fecha_cotrato','monto_uvi', 'valor_uvi_contrato']


class EmpresaPolizaForm(ModelForm):
    class Meta:
        model = EmpresaPoliza
        fields = ['empresa', 'location', 'telefono']


class CertificadoForm(ModelForm):
    class Meta:
        model = Certificados
        fields = ['obra', 'nro_cert', 'fecha_acta', 'fecha', 'uvi','avance_acum_proy']
        widgets = {'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'fecha_acta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})}


class CertificadoFormEdit(ModelForm):
    class Meta:
        model = Certificados
        fields = ['obra', 'nro_cert', 'fecha_acta', 'fecha', 'uvi']
        # fields = '__all__'


class ActasObrasForm(ModelForm):
    class Meta:
        model = ActasObras
        fields = '__all__'
        widgets = {'fecha': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}


class ActasObrasFormEdit(ModelForm):
    class Meta:
        model = ActasObras
        fields = ['obra', 'tipo', 'fecha', 'orden', 'dispo']


class PolizaForm(ModelForm):
    class Meta:
        model = Polizas
        exclude = ['codPol', 'user', 'orden']


class MemoriaForm(ModelForm):
    class Meta:
        model = Memorias
        fields = ['obra', 'memoria', 'resumen', 'imagen']

class DispoInspForm(ModelForm):
    class Meta:
        model = DispoInspector
        exclude = ['id', 'user']
        widgets = {'fecha': forms.DateInput(
            attrs={'class': 'form-control','type': 'date'})}

class DispoInspFormEdit(ModelForm):
    class Meta:
        model = DispoInspector
        exclude = ['id', 'user']
