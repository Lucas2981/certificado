from django.forms import DateInput, ModelForm
from .models import Obras,EmpresaPoliza, Certificados
from django import forms

class ObraFormAll(ModelForm):
    class Meta:
        model = Obras
        fields = '__all__'
class ObraFormActas(ModelForm):
    class Meta:
        model = Obras
        fields = ['acta_inicio', 'ampliacion_1','ampliacion_2','vencimiento_ampliacion_1','vencimiento_ampliacion_2','acta_ampliacion_1','acta_ampliacion_2','monto_contrato','fecha_cotrato','monto_uvi','valor_uvi_contrato','acta_fondo_reparo','poliza_sustitucion','empresa_poliza','tiene_poliza']
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



