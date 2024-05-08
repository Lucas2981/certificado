from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.index, name='index'),
    path('obras/',login_required(views.obras), name='obras'),
    path('obras/detalle/<int:pk>/',login_required(views.obra_detalle), name='obra_detalle'),
    path('obras/poliza/<int:pk>/',login_required(views.obra_poliza), name='obra_poliza'),
    path('obras/certificados/',login_required(views.certificados_lista), name='certificados'),
    path('obras/certificados/<int:obra_id>/',login_required(views.certificados_lista_obra), name='certificados_obra'),
    path('obras/certificados/nuevo',login_required(views.create_certificado), name='nuevo_cert'),
    path('obras/certificados/<int:pk>/editar/',login_required(views.edit_certificado), name='editar_cert'),
    path('obras/certificados/<int:pk>/eliminar/',login_required(views.delete_certificado), name='eliminar_cert'),
    path('aseguradora/',login_required(views.lista_empresa), name='aseguradora'),
    path('aseguradora/nueva',login_required(views.create_empresa), name='nueva'),
    path('aseguradora/editar/<int:pk>/',login_required(views.edit_empresa), name='editar'),

]