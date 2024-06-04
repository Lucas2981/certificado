from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',login_required(views.index), name='index'),
    # obras
    path('obras/',login_required(views.lista_obras), name='obras'),
    path('obras/detalle/',login_required(views.detalle_obra), name='obra_detalle'),
    path('obras/nueva',login_required(views.crear_obra), name='nueva_obra'),
    path('obras/<int:pk>/editar/',login_required(views.editar_obra), name='editar_obra'),
    # certificados
    path('obras/certificados/',login_required(views.lista_certificados), name='certificados'),
    path('obras/certificados/<int:obra_id>/',login_required(views.lista_certificados_obra), name='certificados_obra'),
    path('obras/certificados/nuevo',login_required(views.crear_certificado), name='nuevo_cert'),
    path('obras/certificados/<int:pk>/editar/',login_required(views.editar_certificado), name='editar_cert'),
    path('obras/certificados/<int:pk>/eliminar/',login_required(views.borrar_certificado), name='eliminar_cert'),
    path('obras/certificados/<int:pk>/ver/',login_required(views.ver_certificado), name='ver_cert'),
    # memorias
    path('obras/memoria/nueva',login_required(views.crear_memoria), name='nueva_memoria'),
    path('obras/memoria/<int:pk>/editar/',login_required(views.editar_memoria), name='editar_memoria'),
    path('obras/memoria/<int:pk>/eliminar/',login_required(views.borrar_memoria), name='eliminar_memoria'),
    path('obras/memoria/',login_required(views.lista_memoria), name='memorias'),
    # actas
    path('obras/certificados/actas/<int:obra_id>/',login_required(views.lista_actas_obra), name='actas_obra'),
    path('obras/certificados/actas/',login_required(views.lista_actas), name='actas'),
    path('obras/certificados/acta/nueva/',login_required(views.crear_acta), name='nueva_acta'),
    path('obras/certificados/acta/<int:pk>/editar/',login_required(views.editar_acta), name='editar_acta'),
    path('obras/certificados/acta/<int:pk>/eliminar/',login_required(views.borrar_acta), name='eliminar_acta'),
    # aseguradoras
    path('aseguradora/',login_required(views.lista_empresa), name='aseguradora'),
    path('aseguradora/nueva',login_required(views.create_empresa), name='nueva'),
    path('aseguradora/<int:pk>//editar',login_required(views.edit_empresa), name='editar'),
    path('aseguradora/<int:pk>/elimiar',login_required(views.borrar_empresa), name='eliminar'),
    # polizas
    path('aseguradora/poliza/nueva/',login_required(views.crear_poliza), name='nueva_poliza'),
    path('aseguradora/poliza/<int:pk>/editar/',login_required(views.editar_poliza), name='editar_poliza'),
    path('aseguradora/poliza/<int:pk>/elimiar/',login_required(views.borrar_poliza), name='eliminar_poliza'),
    path('aseguradora/poliza/',login_required(views.lista_poliza), name='poliza'),
    # dispo inspectores
    path('obras/dispo/nueva',login_required(views.crear_dispo_inspector), name='nueva_dispo_inspe'),
    path('obras/dispo/<int:pk>/editar/',login_required(views.editar_dispo_inspector), name='editar_dispo_inspe'),
    path('obras/dispo/<int:pk>/elimiar/',login_required(views.borrar_dispo_inspector), name='eliminar_dispo_inspe'),
    path('obras/dispo/',login_required(views.lista_dispo_inspector), name='dispo_inspe'),
    path('obras/dispo/<int:obra_id>/',login_required(views.lista_dispo_inspector_obra), name='dispo_inspe_obra'),
    # Mediciones
    path('obras/medicion/nueva',login_required(views.crear_actas_obras), name='nueva_medicion'),
    path('obras/medicion/<int:pk>/editar/',login_required(views.editar_actas_obras), name='editar_medicion'),
    path('obras/medicion/<int:pk>/elimiar/',login_required(views.borrar_actas_obras), name='eliminar_medicion'),
    path('obras/medicion/',login_required(views.lista_actas_obras), name='medicion'),
]