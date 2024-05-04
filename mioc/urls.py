from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.index, name='index'),
    path('obras/',login_required(views.obras), name='obras'),
    path('obras/detalle/<int:pk>/',login_required(views.obra_detalle), name='obra_detalle'),
    path('aseguradora/',login_required(views.lista_empresa), name='aseguradora'),
    path('aseguradora/nueva',login_required(views.create_empresa), name='nueva'),
    path('aseguradora/editar/<int:pk>/',login_required(views.edit_empresa), name='editar'),

]