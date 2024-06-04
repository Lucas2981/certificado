from django.forms import DateInput, ModelForm
from .models import ActaMedicion, ActasObras, DispoInspector, Memorias, Obras, EmpresaPoliza, Certificados, Polizas, Instituciones
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
        fields = ['expediente','obra', 'nro_cert', 'fecha_acta', 'fecha', 'uvi','avance_acum_proy']
        widgets = {'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'fecha_acta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'expediente': forms.TextInput(attrs={'placeholder': 'EX-20XX-00XXXX- -CAT-MIOC'})}

class CertificadoFormEdit(ModelForm):
    class Meta:
        model = Certificados
        fields = ['expediente','obra', 'nro_cert', 'fecha_acta', 'fecha', 'uvi']
        # fields = '__all__'

class CertificadoViewForm(ModelForm):
    class Meta:
        model = Certificados
        fields = '__all__'
        widgets = {
            "expediente": forms.TextInput(attrs={"readonly": True}),
            "obra": forms.Select(attrs={"readonly": True}),
            "nro_cert": forms.TextInput(attrs={"readonly": True}),
            "codCert": forms.TextInput(attrs={"readonly": True}),
            "fecha_acta": forms.TextInput(attrs={"readonly": True}),
            "fecha": forms.TextInput(attrs={"readonly": True}),
            "uvi": forms.TextInput(attrs={"readonly": True}),
            "uvi_acum": forms.TextInput(attrs={"readonly": True}),
            "avance_acum_proy": forms.TextInput(attrs={"readonly": True}),
            "avance_acum_med": forms.TextInput(attrs={"readonly": True}),
            "coef_avance": forms.TextInput(attrs={"readonly": True}),
            "cargaCert": forms.Select(attrs={"readonly": True}),
            "periodo": forms.TextInput(attrs={"readonly": True}),
            'ultimo_editor': forms.Select(attrs={"readonly": True}),
            'ultima_modificacion': forms.TextInput(attrs={"readonly": True}),
        }

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

class ActaMedicionForm(ModelForm):
    class Meta:
        model = ActaMedicion
        fields = ['obra', 'acta_nro', 'periodo']
        widgets = {'periodo': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}
class ActaMedicionFormEdit(ModelForm):
    class Meta:
        model = ActaMedicion
        fields = ['obra', 'acta_nro', 'periodo']
