from django.forms import DateInput, ModelForm
from .models import ActaMedicion, ActaMedicionValidacion,  ActasInicio, AnticipoFinanciero, CertificadosAF, DispoInspector, DispoParalizacion, DispoReinicio, Estructuras, Memorias, Obras, EmpresaPoliza, Certificados, PlanTrabajo, Polizas, Instituciones, dispo_plan_trabajo, dispoCertAF, facturasAF
from django import forms
# llamar librerias de admin para autocompletar
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin


class ObraFormAll(ModelForm):
    class Meta:
        model = Obras
        fields = '__all__'
        widgets = {
            'inicio': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_cotrato': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),}

class ObraFormAllEdit(ModelForm):
    class Meta:
        model = Obras
        fields = '__all__'

class ObraFormActas(ModelForm):
    class Meta:
        model = Obras
        fields = ['monto_contrato', 'fecha_cotrato','monto_uvi', 'valor_uvi_contrato']

class EmpresaPolizaForm(ModelForm):
    class Meta:
        model = EmpresaPoliza
        exclude = ['creaEmpresa',]

class CertificadoForm(ModelForm):
    class Meta:
        model = Certificados
        fields = ['expediente','acta']
        widgets = {'expediente': forms.TextInput(attrs={'placeholder': 'EX-20XX-00XXXX- -CAT-MIOC'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = ActaMedicion.objects.filter(certificados__isnull=True,actamedicionvalidacion__validated=True).values_list('acta', flat=True)
        self.fields['acta'].queryset = ActaMedicion.objects.filter(acta__in=obras_ids)

class CertificadoViewForm(ModelForm):
    class Meta:
        model = Certificados
        fields = '__all__'

class PolizaForm(ModelForm):
    class Meta:
        model = Polizas
        exclude = ['codPol', 'user', 'orden']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = Obras.objects.filter(polizas__isnull=True).values_list('codObra', flat=True)
        self.fields['obra'].queryset = Obras.objects.filter(codObra__in=obras_ids)

class PolizaFormEdit(ModelForm):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = Obras.objects.filter(dispoinspector__inspector__isnull=True).values_list('codObra', flat=True)
        self.fields['obra'].queryset = Obras.objects.filter(codObra__in=obras_ids)

class DispoInspFormEdit(ModelForm):
    class Meta:
        model = DispoInspector
        exclude = ['id', 'user']

class ActaMedicionForm(ModelForm):
    class Meta:
        model = ActaMedicion
        fields = ['obra', 'acta', 'periodo']
        widgets = {'periodo': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}

class ActaMedicionFormEdit(ModelForm):
    class Meta:
        model = ActaMedicion
        fields = ['obra', 'acta', 'periodo']

class ActaMedicionValidatedForm(ModelForm):
    class Meta:
        model = ActaMedicionValidacion
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        obras_ids = ActaMedicion.objects.filter(actamedicionvalidacion__isnull=True).values_list('acta', flat=True)
        self.fields['acta'].queryset = ActaMedicion.objects.filter(acta__in=obras_ids)

class ActaMedicionValidatedFormEdit(ModelForm):
    class Meta:
        model = ActaMedicionValidacion
        fields = '__all__'

class ActaInicioForm(ModelForm):
    class Meta:
        model = ActasInicio
        fields = ['obra','fecha']
        widgets = {'fecha': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = Obras.objects.filter(dispoinspector__inspector__isnull=False, actasinicio__isnull=True).values_list('codObra', flat=True)
        self.fields['obra'].queryset = Obras.objects.filter(codObra__in=obras_ids)

class ActaInicioFormEdit(ModelForm):
    class Meta:
        model = ActasInicio
        fields = ['obra','fecha']

class AntidipoFinancieroForm(ModelForm):
    class Meta:
        model = AnticipoFinanciero
        fields = ['obra','anticipo','dispo','porcentaje','fecha']
        widgets = {'fecha': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = Obras.objects.filter(anticipofinanciero__isnull=True).values_list('codObra', flat=True)
        self.fields['obra'].queryset = Obras.objects.filter(codObra__in=obras_ids)

class AntidipoFinancieroFormEdit(ModelForm):
    class Meta:
        model = AnticipoFinanciero
        fields = ['obra','anticipo','dispo','porcentaje','fecha']

class CertificadoAFForm(ModelForm):
    class Meta:
        model = CertificadosAF
        fields = ('dispo','expediente','fecha')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = AnticipoFinanciero.objects.filter(certificadosaf__isnull=True).values_list('dispo', flat=True)
        self.fields['dispo'].queryset = AnticipoFinanciero.objects.filter(dispo__in=obras_ids)

class CertificadoAFFormEdit(ModelForm):
    class Meta:
        model = CertificadosAF
        fields = ('dispo','expediente','fecha','monto')

class EstructuraForm(ModelForm):
    class Meta:
        model = Estructuras
        fields = ('obra','link','fecha')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = Obras.objects.filter(estructuras__isnull=True).values_list('codObra', flat=True)
        self.fields['obra'].queryset = Obras.objects.filter(codObra__in=obras_ids)

class EstructuraFormEdit(ModelForm):
    class Meta:
        model = Estructuras
        fields = ('obra','link','fecha')

class DispoCertAFForm(ModelForm):
    class Meta:
        model = dispoCertAF
        fields = ('certificado','dispo','fecha','observacion')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        # Lógica para filtrar las opciones del campo obra
        obras_ids = CertificadosAF.objects.filter(dispocertaf__isnull=True,facturasaf__isnull=False).values_list('dispo', flat=True)
        self.fields['certificado'].queryset = CertificadosAF.objects.filter(dispo__in=obras_ids)

class DispoCertAFFormEdit(ModelForm):
    class Meta:
        model = dispoCertAF
        fields = ('certificado','dispo','fecha','observacion')

class FacturasAFForm(ModelForm):
    class Meta:
        model = facturasAF
        fields = ('certificado','tipo','pto_venta','comprobante','fecha','cuit','monto')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        obras_ids = CertificadosAF.objects.filter(facturasaf__isnull=True).values_list('dispo', flat=True)
        self.fields['certificado'].queryset = CertificadosAF.objects.filter(dispo__in=obras_ids)

class FacturasAFFormEdit(ModelForm):
    class Meta:
        model = facturasAF
        fields = ('certificado','tipo','pto_venta','comprobante','fecha','cuit','monto')

class dispo_plan_trabajoForm(ModelForm):
    class Meta:
        model = dispo_plan_trabajo
        fields = ('obra','instrumento','fecha_aplicacion')
        widgets = {'fecha_aplicacion': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        obras_ids = Obras.objects.filter(dispo_plan_trabajo__isnull=True).values_list('codObra', flat=True)
        self.fields['obra'].queryset = Obras.objects.filter(codObra__in=obras_ids)
        
class dispo_plan_trabajo_2Form(ModelForm):
    class Meta:
        model = dispo_plan_trabajo
        fields = ('obra','instrumento','fecha_aplicacion','tipo')
        widgets = {'fecha_aplicacion': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}

class dispo_plan_trabajoFormEdit(ModelForm):
    class Meta:
        model = dispo_plan_trabajo
        fields = ('obra','instrumento','fecha_aplicacion','tipo')

class PlanTrabajoForm(ModelForm):
    class Meta:
        model = PlanTrabajo
        fields = ('dispo_plan','periodoNro','fechaPeriodo','uvisEsperados')
        widgets = {'fechaPeriodo': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()
    def limitar_opciones_obra(self):
        obras_ids = Obras.objects.filter(actasinicio__isnull=False).values_list('codObra', flat=True)
        self.fields['dispo_plan'].queryset = dispo_plan_trabajo.objects.filter(obra__codObra__in=obras_ids).distinct().exclude(plantrabajo__ultimo=True)
class DispoParalizacionForm(ModelForm):
    class Meta:
        model = DispoParalizacion
        exclude = ['user']
        widgets = {'fecha_paralizacion': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()

    def limitar_opciones_obra(self):
        obras_ids = Obras.objects.filter(dispo_plan_trabajo__isnull=False).values_list('codObra', flat=True)
        self.fields['dispo_plan'].queryset = dispo_plan_trabajo.objects.filter(obra__codObra__in=obras_ids, dispoparalizacion__isnull=True)
class DispoParalizacionFormEdit(ModelForm):
    class Meta:
        model = DispoParalizacion
        exclude = ['user']

class DispoReinicioForm(ModelForm):
    class Meta:
        model = DispoReinicio
        fields = ('dispo','dispo_para','fecha_reinicio')
        widgets = {'fecha_reinicio': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limitar_opciones_obra()
    def limitar_opciones_obra(self):
        obras_ids = Obras.objects.filter(dispo_plan_trabajo__isnull=False).values_list('codObra', flat=True)
        self.fields['dispo_para'].queryset = DispoParalizacion.objects.filter(dispo_plan__obra__codObra__in=obras_ids,disporeinicio__isnull=True)

class DispoReinicioFormEdit(ModelForm):
    class Meta:
        model = DispoReinicio
        fields = ('dispo','dispo_para','fecha_reinicio')

