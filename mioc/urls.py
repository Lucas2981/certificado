from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.index, name='index'),
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
    # memorias
    path('obras/memoria/nueva',login_required(views.crear_memoria), name='nueva_memoria'),
    path('obras/memoria/<int:pk>/editar/',login_required(views.editar_memoria), name='editar_memoria'),
    # actas
    path('obras/certificados/actas/<int:obra_id>/',login_required(views.lista_actas_obra), name='actas_obra'),
    path('obras/certificados/actas/',login_required(views.lista_actas), name='actas'),
    path('obras/certificados/acta/nueva/',login_required(views.crear_acta), name='nueva_acta'),
    path('obras/certificados/acta/<int:pk>/editar/',login_required(views.editar_acta), name='editar_acta'),
    # aseguradoras
    path('aseguradora/',login_required(views.lista_empresa), name='aseguradora'),
    path('aseguradora/nueva',login_required(views.create_empresa), name='nueva'),
    path('aseguradora/<int:pk>//editar',login_required(views.edit_empresa), name='editar'),
    # polizas
    path('aseguradora/poliza/nueva/',login_required(views.crear_poliza), name='nueva_poliza'),
    path('aseguradora/poliza/<int:pk>/editar/',login_required(views.editar_poliza), name='editar_poliza'),
    path('aseguradora/poliza/<int:pk>/elimiar/',login_required(views.borrar_poliza), name='eliminar_poliza'),
    path('aseguradora/poliza/',login_required(views.lista_poliza), name='poliza'),
]