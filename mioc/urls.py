from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.index, name='index'),
    # obras
    path('obras/',login_required(views.obras), name='obras'),
    path('obras/detalle/',login_required(views.obra_detalle), name='obra_detalle'),
    path('obras/poliza/<int:pk>/',login_required(views.obra_poliza), name='obra_poliza'),
    # certificados
    path('obras/certificados/',login_required(views.certificados_lista), name='certificados'),
    path('obras/certificados/<int:obra_id>/',login_required(views.certificados_lista_obra), name='certificados_obra'),
    path('obras/certificados/nuevo',login_required(views.create_certificado), name='nuevo_cert'),
    path('obras/certificados/<int:pk>/editar/',login_required(views.edit_certificado), name='editar_cert'),
    path('obras/certificados/<int:pk>/eliminar/',login_required(views.delete_certificado), name='eliminar_cert'),
    # actas
    path('obras/certificados/actas/<int:obra_id>/',login_required(views.actas_lista_obras), name='actas_obra'),
    path('obras/certificados/actas/',login_required(views.actas_lista), name='actas'),
    path('obras/certificados/acta/nueva/',login_required(views.actas_obras), name='nueva_acta'),
    path('obras/certificados/acta/<int:pk>/editar/',login_required(views.actas_obras_editar), name='editar_acta'),
    # aseguradoras
    path('aseguradora/',login_required(views.lista_empresa), name='aseguradora'),
    path('aseguradora/nueva',login_required(views.create_empresa), name='nueva'),
    path('aseguradora/editar/<int:pk>/',login_required(views.edit_empresa), name='editar'),
    # polizas
    path('aseguradora/poliza/nueva/',login_required(views.poliza_nueva), name='nueva_poliza'),
]