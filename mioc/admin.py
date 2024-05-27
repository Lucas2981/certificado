from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import (ActaTipo, ActasObras, Certificados, DispoInspector, Empresas, Estados, Location,Clases,Instituciones, Memorias, Polizas,Titulos,Inspectores,Obras,Rubros,
                    Subrubros,Presupuestos,PresupuestosSubrubros,Uvis,Unidades,EmpresaPoliza)

# Register your models here.
class LocalidadAdmin(ImportExportModelAdmin):
    list_display = ('NOMLOC','NOMMUNI','NOMDEPTO')
    search_fields = ('CODPROV', 'NOMPROV', 'CODDEPTO', 'NOMDEPTO', 'CODMUNI', 'NOMMUNI', 'CODLOC', 'CODAGLO', 'NOMLOC')
    list_filter = ('NOMDEPTO', 'NOMMUNI','NOMLOC')
    ordering = ['CODPROV', 'CODDEPTO', 'CODMUNI', 'CODLOC']
class LocalidadExport(resources.ModelResource):
    class Meta:
        model = Location
        fields = ('CODPROV', 'NOMPROV', 'CODDEPTO', 'NOMDEPTO', 'CODMUNI', 'NOMMUNI', 'CODLOC', 'CODAGLO', 'NOMLOC')
admin.site.register(Location,LocalidadAdmin)

class ClasesAdmin(admin.ModelAdmin):
    list_display = ('name','subname')
    search_fields = ('name', 'subname')
    list_filter = ('name', 'subname')
    ordering = ['name']
admin.site.register(Clases,ClasesAdmin)

class EstadosAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']
admin.site.register(Estados,EstadosAdmin)

class InstitucionesAdmin(ImportExportModelAdmin):
    list_display = ('name','clase','location')
    search_fields = ('name', )
    list_filter = ('name', 'clase__name','location__NOMDEPTO','location__NOMMUNI','location__NOMLOC')
    ordering = ['name']
    raw_id_fields = ['location']
class InstitucionesExport(resources.ModelResource):
    class Meta:
        model = Instituciones
        search_fields = ('name', 'clase', 'location')
        fields = ('name', 'clase', 'location')
        ordering = ['name']
admin.site.register(Instituciones,InstitucionesAdmin)

class TitulosAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']
admin.site.register(Titulos,TitulosAdmin)

class InspectoresAdmin(admin.ModelAdmin):
    list_display = ('fullname','dni','telephone','email')
    search_fields = ('titulo','name','surname','dni','telephone','email')
    list_filter = ('titulo__name', 'fullname')
    ordering = ['surname']
admin.site.register(Inspectores,InspectoresAdmin)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('name','propietario','location','telephone','email')
    search_fields = ('name',)
    ordering = ['name']
    raw_id_fields = ['location']
admin.site.register(Empresas,EmpresaAdmin)

class ObrasAdmin(admin.ModelAdmin):
    list_display = ('codObra','institucion','inicio','plazo','vencimiento_contractual','uvi')
    search_fields = ('institucion',)
    autocomplete_fields = ['institucion']
    list_filter = ('institucion__name',)
    ordering = ['institucion']
admin.site.register(Obras,ObrasAdmin)

class RubrosAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    search_fields = ('name',)
    ordering = ['name']
admin.site.register(Rubros,RubrosAdmin)

class SubrubrosAdmin(admin.ModelAdmin):
    list_display = ('id','name','rubro')
    search_fields = ('name',)
    list_filter = ('rubro__name',)
    ordering = ['rubro','name']
admin.site.register(Subrubros,SubrubrosAdmin)

class PresupuestoSubrubroInline(admin.TabularInline):
    model = PresupuestosSubrubros
    extra = 0
    autocomplete_fields = ['rubro','subrubro']

class PresupuestosAdmin(admin.ModelAdmin):
    inlines = [PresupuestoSubrubroInline]
    # def inspector(self, obj):
    #     return obj.obra.inspector  
    # inspector.short_description = 'Inspector'
    def codObra(self, obj):
        return obj.obra.codObra
    codObra.short_description = 'Cod. Obra'
    list_display = ('id','codObra','obra','uvi')
    search_fields = ('obra','rubro','subrubro','presupuesto','presupuesto_subrubro')
    list_filter = ('obra__institucion__name',)
    ordering = ['obra',]
    list_display_links = ['codObra','id']
    # def get_readonly_fields(self, request, obj=None):
    #     return ['subrubro']
admin.site.register(Presupuestos,PresupuestosAdmin)

class UvisAdmin(admin.ModelAdmin):
    list_display = ('fecha','valor')
    search_fields = ('fecha','valor')
    ordering = ['fecha']
admin.site.register(Uvis,UvisAdmin)

class UnidadesAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)
    ordering = ['name']
admin.site.register(Unidades,UnidadesAdmin)

class EmpresaPolizaAdmin(admin.ModelAdmin):
    list_display = ('id','empresa','creaEmpresa')
admin.site.register(EmpresaPoliza,EmpresaPolizaAdmin)

class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('codCert','id','obra','nro_cert','periodo','uvi')
admin.site.register(Certificados,CertificadoAdmin)

class ActaTipoAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']
admin.site.register(ActaTipo,ActaTipoAdmin)

class ActaObrasAdmin(admin.ModelAdmin):
    list_display = ('codActa','obra','tipo','fecha','dispo')
admin.site.register(ActasObras,ActaObrasAdmin)

class PolizaAdmin(admin.ModelAdmin):
    list_display = ('codPol','obra','empresa_poliza')
admin.site.register(Polizas,PolizaAdmin)

class MemoriasAdmin(admin.ModelAdmin):
    list_display = ('id','obra')
admin.site.register(Memorias,MemoriasAdmin)

class DispoInspectorAdmin(admin.ModelAdmin):
    list_display = ('dispo','inspector')
admin.site.register(DispoInspector,DispoInspectorAdmin)