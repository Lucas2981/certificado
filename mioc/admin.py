from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Location,Clases,Instituciones,Titulos,Inspectores,Obras

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

class InstitucionesAdmin(ImportExportModelAdmin):
    list_display = ('name','clase','location')
    search_fields = ('name', 'clase', 'location')
    list_filter = ('name', 'clase', 'location')
    ordering = ['name']
    raw_id_fields = ['location']
class InstitucionesExport(resources.ModelResource):
    class Meta:
        model = Instituciones
        fields = ('name', 'clase', 'location')
admin.site.register(Instituciones,InstitucionesAdmin)

class TitulosAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']
admin.site.register(Titulos,TitulosAdmin)

class InspectoresAdmin(admin.ModelAdmin):
    list_display = ('titulo','name','surname','dni','telephone','mail')
    search_fields = ('titulo','name','surname','dni','telephone','mail')
    list_filter = ('titulo', 'surname')
    ordering = ['surname']
admin.site.register(Inspectores,InspectoresAdmin)

class ObrasAdmin(admin.ModelAdmin):
    list_display = ('institucion','inicio','plazo','vencimiento_contractual','ampliacion_1','vencimiento_ampliacion_1','ampliacion_2','vencimiento_ampliacion_2')
    search_fields = ('institucion','inspector')
    list_filter = ('institucion','inspector')
    ordering = ['institucion']
admin.site.register(Obras,ObrasAdmin)