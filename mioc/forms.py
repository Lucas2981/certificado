from django.forms import ModelForm
from .models import Obras
from django import forms

class ObraFormAll(ModelForm):
    class Meta:
        model = Obras
        fields = '__all__'
class ObraFormActas(ModelForm):
    class Meta:
        model = Obras
        fields = ['acta_inicio', 'ampliacion_1','ampliacion_2','vencimiento_ampliacion_1','vencimiento_ampliacion_2','acta_ampliacion_1','acta_ampliacion_2','monto_contrato','fecha_cotrato','monto_uvi','valor_uvi_contrato']
        