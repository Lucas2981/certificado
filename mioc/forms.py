from django.forms import DateInput, ModelForm
from .models import ActasObras, Obras,EmpresaPoliza, Certificados, Polizas
from django import forms

class ObraFormAll(ModelForm):
    class Meta:
        model = Obras
        fields = '__all__'
class ObraFormActas(ModelForm):
    class Meta:
        model = Obras
        fields = ['monto_contrato','fecha_cotrato','monto_uvi','valor_uvi_contrato']
class EmpresaPolizaForm(ModelForm):
    class Meta:
        model =  EmpresaPoliza     
        fields = ['empresa','location','telefono']

class CertificadoForm(ModelForm):
    class Meta:
        model = Certificados
        fields = ['obra','nro_cert','fecha_acta','fecha','uvi']
        widgets = {'fecha': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
                    'fecha_acta': forms.DateInput(attrs={'class': 'form-control','type': 'date'})}

class CertificadoFormEdit(ModelForm):
    class Meta:
        model = Certificados
        fields = ['obra','nro_cert','fecha_acta','fecha','uvi']

class ActasObrasForm(ModelForm):
    class Meta:
        model = ActasObras
        fields = '__all__'
        widgets = {'fecha': forms.DateInput(attrs={'class': 'form-control','type': 'date'})}

class ActasObrasFormEdit(ModelForm):
    class Meta:
        model = ActasObras
        fields = ['obra','tipo','fecha','orden','dispo']

class PolizaForm(ModelForm):
    class Meta:
        model =  Polizas     
        exclude = ['codPol','user']


