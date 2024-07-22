from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',login_required(views.index), name='index'),
    path('dashboard/',views.dashboard, name='dashboard'),
    # obras
    path('obras/',login_required(views.lista_obras), name='obras'),
    path('obras/detalle/',login_required(views.detalle_obra), name='obra_detalle'),
    path('obras/nueva',login_required(views.crear_obra), name='nueva_obra'),
    path('obras/<int:pk>/editar/',login_required(views.editar_obra), name='editar_obra'),
    # Disposiciones de Paralización
    path('obras/dispo_paralizacion/nueva',login_required(views.crear_dispo_paralizacion), name='nueva_dispo_paralizacion'),
    path('obras/dispo_paralizacion/',login_required(views.lista_dispo_paralizacion), name='dispo_paral'),
    path('obras/dispo_paralizacion/<int:pk>/editar/',login_required(views.editar_dispo_paralizacion), name='editar_dispo_paralizacion'),
    path('obras/dispo_paralizacion/<int:pk>/eliminar/',login_required(views.borrar_dispo_paralizacion), name='eliminar_dispo_paralizacion'),
    # Disposiciones de Reinicio
    path('obras/dispo_reinicio/',login_required(views.lista_dispo_reinicio), name='dispo_reinicio'),
    path('obras/dispo_reinicio/<int:pk>/editar/',login_required(views.editar_dispo_reinicio), name='editar_dispo_reinicio'),
    path('obras/dispo_reinicio/<int:pk>/eliminar/',login_required(views.borrar_dispo_reinicio), name='eliminar_dispo_reinicio'),
    path('obras/dispo_reinicio/nueva',login_required(views.crear_dispo_reinicio), name='nueva_dispo_reinicio'),
    # Disposiciones Plan de trabajos
    path('obras/dispo_plan_trabajo/',login_required(views.lista_dispo_plan_trabajo), name='lista_dispo_plan_trabajo'),
    path('obras/dispo_plan_trabajo/optimizado/',login_required(views.lista_dispo_plan_trabajo_2), name='lista_dispo_plan_trabajo_2'),
    path('obras/dispo_plan_trabajo/<int:pk>/editar/',login_required(views.editar_dispo_plan_trabajo), name='editar_dispo_plan_trabajo'),
    path('obras/dispo_plan_trabajo/<int:pk>/editar/optimizado',login_required(views.editar_dispo_plan_trabajo_2), name='editar_dispo_plan_trabajo_2'),
    path('obras/dispo_plan_trabajo/<int:pk>/eliminar/',login_required(views.borrar_dispo_plan_trabajo), name='eliminar_dispo_plan_trabajo'),
    path('obras/dispo_plan_trabajo/<int:pk>/eliminar/optimizado',login_required(views.borrar_dispo_plan_trabajo_2), name='eliminar_dispo_plan_trabajo_2'),
    path('obras/dispo_plan_trabajo/nuevo',login_required(views.crear_dispo_plan_trabajo), name='nuevo_dispo_plan_trabajo'),
    path('obras/dispo_plan_trabajo/nuevo/optimizado',login_required(views.crear_dispo_plan_trabajo_2), name='nuevo_dispo_plan_trabajo_2'),
    # Planes de Trabajo mensuales
    path('obras/plan_trabajo/',login_required(views.lista_plan_trabajo), name='lista_plan_trabajo'),
    path('obras/plan_trabajo/<int:pk>/editar/',login_required(views.editar_plan_trabajo), name='editar_plan_trabajo'),
    path('obras/plan_trabajo/nuevo',login_required(views.crear_plan_trabajo), name='nuevo_plan_trabajo'),
    path('obras/plan_trabajo/<int:pk>/eliminar/',login_required(views.borrar_plan_trabajo), name='borrar_plan_trabajo'),
    # Facturas AF
    path('obras/facturas_AF/nueva',login_required(views.crear_factura_af), name='nueva_factura_AF'),
    path('obras/facturas_AF/<int:pk>/editar/',login_required(views.editar_factura_AF), name='editar_factura_AF'),
    path('obras/facturas_AF/<int:pk>/eliminar/',login_required(views.borrar_factura_AF), name='eliminar_factura_AF'),
    path('obras/facturas_AF/',login_required(views.lista_factura_AF), name='facturas_AF'),
    # certificados
    path('obras/certificados/',login_required(views.lista_certificados), name='certificados'),
    path('obras/certificados/<int:obra_id>/',login_required(views.lista_certificados_obra), name='certificados_obra'),
    path('obras/certificados/nuevo',login_required(views.crear_certificado), name='nuevo_cert'),
    path('obras/certificados/<int:pk>/editar/',login_required(views.editar_certificado), name='editar_cert'),
    path('obras/certificados/<int:pk>/eliminar/',login_required(views.borrar_certificado), name='eliminar_cert'),
    path('obras/certificados/<int:pk>/ver/',login_required(views.ver_certificado), name='ver_cert'),
    # anticipo
    path('obras/certificados/anticipo/nuevo',login_required(views.crear_certificado_AF), name='nuevo_certificado_AF'),
    path('obras/certificados/anticipo/<int:pk>/editar/',login_required(views.editar_certificado_AF), name='editar_certificado_AF'),
    path('obras/certificados/anticipo/<int:pk>/eliminar/',login_required(views.borrar_certificado_AF), name='eliminar_certificado_AF'),
    path('obras/certificados/anticipo/',login_required(views.lista_certificados_AF), name='certificado_AF'),
    # memorias
    path('obras/memoria/nueva',login_required(views.crear_memoria), name='nueva_memoria'),
    path('obras/memoria/<int:pk>/editar/',login_required(views.editar_memoria), name='editar_memoria'),
    path('obras/memoria/<int:pk>/eliminar/',login_required(views.borrar_memoria), name='eliminar_memoria'),
    path('obras/memoria/',login_required(views.lista_memoria), name='memorias'),
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
    # Disposiciones inspectores
    path('obras/dispo/nueva',login_required(views.crear_dispo_inspector), name='nueva_dispo_inspe'),
    path('obras/dispo/<int:pk>/editar/',login_required(views.editar_dispo_inspector), name='editar_dispo_inspe'),
    path('obras/dispo/<int:pk>/elimiar/',login_required(views.borrar_dispo_inspector), name='eliminar_dispo_inspe'),
    path('obras/dispo/',login_required(views.lista_dispo_inspector), name='dispo_inspe'),
    path('obras/dispo/<int:obra_id>/',login_required(views.lista_dispo_inspector_obra), name='dispo_inspe_obra'),
    # Disposiciones Anticipo Financiero
    path('obras/dispo/anticipo/nueva',login_required(views.crear_anticipo), name='nuevo_anticipo'),
    path('obras/dispo/anticipo/<int:pk>/editar/',login_required(views.editar_anticipo), name='editar_anticipo'),
    path('obras/dispo/anticipo/<int:pk>/elimiar/',login_required(views.borrar_anticipo), name='eliminar_anticipo'),
    path('obras/dispo/anticipo/',login_required(views.lista_anticipo), name='anticipo'),
    # Disposiciones certificado AF
    path('obras/dispo/certificado_AF/nueva',login_required(views.crear_dispo_cert_af), name='nueva_dispo_certificado_AF'),
    path('obras/dispo/certificado_AF/<int:pk>/editar/',login_required(views.editar_dispo_cert_af), name='editar_dispo_certificado_AF'),
    path('obras/dispo/certificado_AF/<int:pk>/elimiar/',login_required(views.borrar_dispo_cert_af), name='eliminar_dispo_certificado_AF'),
    path('obras/dispo/certificado_AF/',login_required(views.lista_dispo_cert_af), name='dispo_certificado_AF'),
    # Mediciones
    path('obras/medicion/nueva',login_required(views.crear_actas_obras), name='nueva_medicion'),
    path('obras/medicion/<int:pk>/editar/',login_required(views.editar_actas_obras), name='editar_medicion'),
    path('obras/medicion/<int:pk>/elimiar/',login_required(views.borrar_actas_obras), name='eliminar_medicion'),
    path('obras/medicion/',login_required(views.lista_actas_obras), name='medicion'),
    path('obras/inicio/nuevo',login_required(views.crear_actas_inicio), name='nuevo_inicio'),
    path('obras/inicio/<int:pk>/editar/',login_required(views.editar_actas_inicio), name='editar_inicio'),
    path('obras/inicio/<int:pk>/elimiar/',login_required(views.borrar_actas_inicio), name='eliminar_inicio'),
    path('obras/inicio/',login_required(views.lista_actas_inicio), name='inicio'),
    # Validación de medición
    path('obras/acta/validar/nueva',login_required(views.validar_acta), name='validar_acta'),
    path('obras/acta/validar/<int:pk>/editar/',login_required(views.editar_validar_acta), name='editar_validar_acta'),
    path('obras/acta/validar/<int:pk>/eliminar',login_required(views.borrar_validar_acta), name='eliminar_validar_acta'),
    path('obras/acta/validar/',login_required(views.lista_validar_acta), name='lista_validar_acta'),
    # Estructuras
    path('obras/estructura/nueva',login_required(views.crear_estructura), name='nueva_estructura'),
    path('obras/estructura/<int:pk>/editar/',login_required(views.editar_estructura), name='editar_estructura'),
    path('obras/estructura/<int:pk>/elimiar/',login_required(views.borrar_estructura), name='eliminar_estructura'),
    path('obras/estructura/',login_required(views.lista_estructura), name='estructuras'),
    path('obras/estructura/inspector/',login_required(views.lista_estructura_inspector), name='estructuras_inspector'),
]