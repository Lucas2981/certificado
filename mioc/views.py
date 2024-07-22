from itertools import count
from django.utils import timezone
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q,Sum
from django.contrib.auth.decorators import  permission_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
import numpy as np
from . models import ActaMedicion, ActaMedicionValidacion, ActasInicio, AnticipoFinanciero, Certificados, CertificadosAF, DispoInspector, DispoParalizacion, DispoReinicio, Estructuras, Memorias, Obras, EmpresaPoliza, PlanTrabajo, Polizas, dispo_plan_trabajo, dispoCertAF, facturasAF
from . forms import ActaInicioForm, ActaInicioFormEdit, ActaMedicionForm, ActaMedicionFormEdit, ActaMedicionValidatedForm, ActaMedicionValidatedFormEdit, AntidipoFinancieroForm, AntidipoFinancieroFormEdit, CertificadoAFForm, CertificadoAFFormEdit, CertificadoForm, CertificadoViewForm, DispoCertAFForm, DispoCertAFFormEdit, DispoInspForm, DispoInspFormEdit, DispoParalizacionForm, DispoParalizacionFormEdit, DispoReinicioForm, DispoReinicioFormEdit, EstructuraForm, EstructuraFormEdit, FacturasAFForm, FacturasAFFormEdit, MemoriaForm, ObraFormAll, ObraFormActas, EmpresaPolizaForm, ObraFormAllEdit, PlanTrabajoForm, PolizaForm, PolizaFormEdit, dispo_plan_trabajo_2Form, dispo_plan_trabajoForm, dispo_plan_trabajoFormEdit
from datetime import datetime, date

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
def index(request):
    # Obras sin plan de trabajo Inicial
    obras_sin_plan_inicial = Obras.objects.filter(dispo_plan_trabajo__isnull=True, actasinicio__isnull=False)
    try:
        if len(obras_sin_plan_inicial) > 0:
            pend_plan_inicial = len(obras_sin_plan_inicial)
        else:
            pend_plan_inicial = ''
    except:
        pend_plan_inicial = ''
    # Planes de trabajo Iniciales a Implementar
    obras_ids = Obras.objects.filter(actasinicio__isnull=False).values_list('codObra', flat=True)
    plan_inicial_a_implementar = dispo_plan_trabajo.objects.filter(obra__codObra__in=obras_ids).distinct().exclude(plantrabajo__ultimo=True)
    try:
        if len(plan_inicial_a_implementar) > 0:
            pend_plan_inicial_imp = len(plan_inicial_a_implementar)
        else:
            pend_plan_inicial_imp = ''
    except:
        pend_plan_inicial_imp = ''
    # Obras sin poliza msj
    obras_sin_poliza = Obras.objects.filter(polizas__isnull=True)
    try:
        if len(obras_sin_poliza) > 0:
            pend_poliza = len(obras_sin_poliza)
        else:
            pend_poliza = ''
    except:
        pend_poliza = ''
    # Obras sin inspector
    obras_sin_inspector = Obras.objects.filter(dispoinspector__isnull=True)
    try:
        if len(obras_sin_inspector) > 0:
            pend_inspector = len(obras_sin_inspector)
        else:
            pend_inspector = ''
    except:
        pend_inspector = ''
    # Obras sin acta de inicio
    obras_sin_acta = Obras.objects.filter(actasinicio__isnull=True, dispoinspector__isnull=False)
    inspectores = DispoInspector.objects.all()
    try:
        if len(obras_sin_acta) > 0:
            pend_acta_inicio = len(obras_sin_acta)
        else:
            pend_acta_inicio = ''
    except:
        pend_acta_inicio = ''
    # Obras sin anticipo definido
    obras_sin_anticipo = Obras.objects.filter(anticipofinanciero__isnull=True, dispoinspector__isnull=False)
    try:
        if len(obras_sin_anticipo) > 0:
            pend_anticipo = len(obras_sin_anticipo)
        else:
            pend_anticipo = ''
    except:
        pend_anticipo = ''
    # Obras sin extructura informada
    sin_estructuras = Obras.objects.filter(estructuras__isnull=True, dispoinspector__isnull=False)
    try:
        if len(sin_estructuras) > 0:
            pend_estructuras = len(sin_estructuras)
        else:
            pend_estructuras = ''
    except:
        pend_estructuras = ''
    # Actas de mediciones para validar
    actas_sin_validar = ActaMedicion.objects.filter(actamedicionvalidacion__isnull=True)
    try:
        if len(actas_sin_validar) > 0:
            pend_acta_validar = len(actas_sin_validar)
        else:
            pend_acta_validar = ''
    except:
        pend_acta_validar = ''
    # Actas de mediciones sin certificado
    obras_sin_certificado = ActaMedicion.objects.filter(actamedicionvalidacion=True)
    try:
        if len(obras_sin_certificado) > 0:
            pend_certificado = len(obras_sin_certificado)
        else:
            pend_certificado = ''
    except:
        pend_certificado = ''
    # Dispos sin certificado de anticipo financiero
    dispo_sin_certificado_AF = AnticipoFinanciero.objects.filter(certificadosaf__isnull=True, anticipo=True)
    try:
        if len(dispo_sin_certificado_AF) > 0:
            pend_AF = len(dispo_sin_certificado_AF)
        else:
            pend_AF = ''
    except:
        pend_AF = ''
    # Certificados sin dispo de aceptación
    certif_af_sin_dispo = CertificadosAF.objects.filter(dispocertaf__isnull=True, facturasaf__isnull=False)
    try:
        if len(certif_af_sin_dispo) > 0:
            pend_dispo_AF = len(certif_af_sin_dispo)
        else:
            pend_dispo_AF = ''
    except:
        pend_dispo_AF = ''
    # Facturas pendientes AF
    sin_facturas_AF = CertificadosAF.objects.filter(facturasaf__isnull=True)
    try:
        if len(sin_facturas_AF) > 0:
            pend_facturas_AF = len(sin_facturas_AF)
        else:
            pend_facturas_AF = ''
    except:
        pend_facturas_AF = ''
    

    context = {
        'obras_sin_plan_inicial':obras_sin_plan_inicial,
        'pend_plan_inicial':pend_plan_inicial,
        'plan_inicial_a_implementar':plan_inicial_a_implementar,
        'pend_plan_inicial_imp':pend_plan_inicial_imp,
        'obras_sin_poliza':obras_sin_poliza,
        'pend_poliza':pend_poliza,
        'obras_sin_inspector':obras_sin_inspector,
        'pend_inspector':pend_inspector,
        'obras_sin_acta':obras_sin_acta,
        'pend_acta_inicio':pend_acta_inicio,
        'inspectores':inspectores,
        'obras_sin_anticipo':obras_sin_anticipo,
        'pend_anticipo':pend_anticipo,
        'sin_estructuras':sin_estructuras,
        'pend_estructuras':pend_estructuras,
        'actas_sin_validar':actas_sin_validar,
        'pend_acta_validar':pend_acta_validar,
        'obras_sin_certificado':obras_sin_certificado,
        'pend_certificado':pend_certificado,
        'dispo_sin_certificado_AF':dispo_sin_certificado_AF,
        'pend_AF':pend_AF,
        'certif_af_sin_dispo':certif_af_sin_dispo,
        'pend_dispo_AF':pend_dispo_AF,
        'pend_facturas_AF':pend_facturas_AF,
        'sin_facturas_AF':sin_facturas_AF,
    }
    return render(request, 'soc/index.html', context)

def dashboard(request):
    ano = date.today().year
    actas = Obras.objects.filter(fecha__year=ano) # ver aqui
    try:
        paralizadas = actas.filter(tipo__name='Paralización').count() - actas.filter(tipo__name='Reinicio').count()
    except:
        paralizadas = 0
    try:
        finalizadas = actas.filter(tipo__name='Recepción Provisoria').count()
    except:
        finalizadas = 0
    activas = actas.filter(tipo__name='Inicio').count() - finalizadas - paralizadas
    totales = activas + paralizadas + finalizadas
    try:
        porc_paralizadas = round(paralizadas / totales * 100, 2)
        porc_finalizadas = round(finalizadas / totales * 100, 2)
        porc_activas = round(activas / totales * 100, 2)
    except:
        porc_paralizadas = 0
        porc_finalizadas = 0
        porc_activas = 0
    certificados = Certificados.objects.filter(acta__periodo__year=ano)
    cant_cert = len(certificados)
    try:
        monto_cert = certificados.aggregate(Sum('uvi'))['uvi__sum']
    except:
        monto_cert = 0
    
    data = Certificados.objects.filter(acta__periodo__year=ano)
    # Grafico de linea ideal para mostrar la evolución de montos certificados por fecha
    dataBar = data.values_list('acta__obra__institucion__name','acta__periodo').annotate(cantidad=Sum('uvi'))
    dfBar = pd.DataFrame(dataBar, columns=['obra','fecha','uvi'])
    config={'toImageButtonOptions': {'filename': 'Montos certificados por fecha',
                                    'responsive': True}
            }
    fig = go.Figure(
        data=[go.Bar(x=dfBar['fecha'],y=dfBar['uvi'])],
        layout=go.Layout(
        title_text='Montos certificados por fecha',
        xaxis_title='Fecha',
        yaxis_title='Monto en miles de UVIs',
    ))
    fig.update_layout(
    autosize=True,
    width=500,
    height=500,)
    bar = fig.to_html(config=config)
    # Grafico de arbol ideal para mostrar la evolución de montos certificados por clase/empresa/obra/certificado
    dataSun = data.values_list('acta__obra__institucion__clase__name','acta__obra__institucion__clase__subname','acta__obra__empresa__name','acta__obra__institucion__name','acta__obra__monto_uvi').annotate(cantidad=Sum('uvi'))
    dfSun = pd.DataFrame(dataSun, columns=['clase','subclase','empresa','obra','monto','uvi'],)
    try:
        media =  dfSun['uvi']/dfSun['monto']
        fig = px.sunburst(dfSun, path=['clase','subclase','empresa','obra','uvi'], values='monto',
                        color='monto', hover_data=['subclase'],
                        color_continuous_scale='plasma',
                        color_continuous_midpoint=np.average(media, weights=dfSun['monto']),
                        title='Certificados/presupuesto')
        config={'toImageButtonOptions': {'filename': 'Certificados/presupuesto'},
                'displaylogo': False
            }
        sun = fig.to_html(config=config)
    except:
        sun = ''
    # Grafico de arbol ideal para mostrar la evolución de montos certificados por clase/obra/certificado
    dfTreemap = dfSun
    try:
        dfTreemap['avance'] = round(dfTreemap['uvi']/dfTreemap['monto']*100,2)
        fig = px.treemap(dfTreemap, path=[px.Constant("Todas las Empresas"), 'empresa','obra','monto','avance'], values='avance',
                        color='avance', hover_data=['empresa'],
                        color_continuous_scale='blues',
                        color_continuous_midpoint=np.average(dfTreemap['avance'], weights=dfTreemap['monto']),
                        title='Avance de Obras agrupado por Empresa')
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        config={'toImageButtonOptions': {'filename': 'Avance de Obras agrupado por Empresa'},
                'displaylogo': False
            }
        Treemap = fig.to_html(config=config)
    except:
        Treemap = ''
    # Grafico de caja y bigotes para mostrar la evolución de coheficiente de avance por obra
    dataBoxplot = data.values_list('acta__obra__empresa__name','acta__obra__institucion__name','avance_acum_proy','avance_acum_med').annotate(cantidad=Sum('uvi'))
    dfBoxplot = pd.DataFrame(dataBoxplot, columns=['empresa','obra','av_proy','av_real','count'])
    try:
        dfBoxplot['coheficiente'] = round(dfBoxplot['av_real'] / dfBoxplot['av_proy'],2)
        fig = px.box(dfBoxplot, x="empresa", y="coheficiente", points="all",title='Coheficientes de Avance por Empresa')
        config={'toImageButtonOptions': {'filename': 'Coheficientes de Avance por Empresa'},
            }
        boxplot = fig.to_html()
    except:
        boxplot = ''
    context = {
        'certificados': certificados,
        'cant_cert': cant_cert,
        'monto_cert': monto_cert,
        'activas': activas,
        'paralizadas': paralizadas,
        'finalizadas': finalizadas,
        'ano': ano,
        'porc_paralizadas': porc_paralizadas,
        'porc_finalizadas': porc_finalizadas,
        'porc_activas': porc_activas,
        'bar': bar,
        'sun':sun,
        'Treemap': Treemap,
        'boxplot': boxplot,
    }
    return render(request, 'soc/dashboard/dashboard.html', context)

# Div Fondo Sustitución
@permission_required('mioc.add_empresapoliza')
def create_empresa(request):
    if request.method == 'GET':
        return render(request, 'soc/polizas/fondo_reparo_crear.html', {
            'form': EmpresaPolizaForm
        })
    else:
        form = EmpresaPolizaForm(request.POST)
        try:
            if form.is_valid():
                nueva_empresa = form.save(commit=False)
                nueva_empresa.creaEmpresa = request.user
                nueva_empresa.save()
                messages.success(request, f'Nueva empresa creada!')
                return redirect('aseguradora')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/polizas/fondo_reparo_crear.html', {
                'form': form,
                'error': error_message
            })
@permission_required('mioc.change_empresapoliza')
def edit_empresa(request, pk):
    if request.method == 'GET':
        asegura = get_object_or_404(EmpresaPoliza, pk=pk)
        form = EmpresaPolizaForm(instance=asegura)
        return render(request, 'soc/polizas/fondo_reparo_editar.html', {
            'form': form,
        })
    else:
        try:
            asegura = get_object_or_404(EmpresaPoliza, pk=pk)
            form = EmpresaPolizaForm(request.POST, instance=asegura)
            form.save()
            messages.success(request, f'Aseguradora {asegura.empresa} editada!')
            return redirect('aseguradora')
        except ValueError:
            asegura = get_object_or_404(EmpresaPoliza, pk=pk)
            form = EmpresaPolizaForm(instance=asegura)
            return render(request, 'soc/polizas/fondo_reparo_editar.html', {
                'form': form,
                'error': 'Error al validar pedido.'
            })
@permission_required('mioc.delete_empresapoliza')
def borrar_empresa(request, pk):
    asegura = get_object_or_404(EmpresaPoliza, pk=pk)
    asegura.delete()
    messages.success(request, f'Aseguradora {asegura.empresa} eliminada!')
    return redirect('aseguradora')
@permission_required('mioc.view_empresapoliza')
def lista_empresa(request):
    empresa = EmpresaPoliza.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(empresa,5)
        empresa = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        empresa = EmpresaPoliza.objects.filter(
            Q(empresa__icontains=queryset) |
            Q(location__icontains=queryset) |
            Q(telefono__icontains=queryset),
        ).distinct().order_by('empresa',)
    return render(request, 'soc/polizas/empresa_lista.html', {'entity': empresa, 'paginator':paginator })
@permission_required('mioc.add_polizas')
def crear_poliza(request):
    if request.method == 'GET':
        form = PolizaForm
        return render(request, 'soc/polizas/poliza_crear.html', {
            'form': form
        })
    else:
        form = PolizaForm(request.POST)
        try:
            if form.is_valid():
                nueva_poliza = form.save(commit=False)
                nueva_poliza.user = request.user
                nueva_poliza.save()
                messages.success(request, f'Nueva poliza creada!')
                return redirect('poliza')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/polizas/poliza_crear.html', {'form': form, 'error': error_message})
@permission_required('mioc.change_polizas')
def editar_poliza(request, pk):
    poliza = get_object_or_404(Polizas, pk=pk)
    if request.method == 'GET':
        form = PolizaFormEdit(instance=poliza)
        return render(request, 'soc/polizas/poliza_editar.html', {
            'form': form
        })
    else:
        try:
            poliza = get_object_or_404(Polizas, pk=pk)
            form = PolizaFormEdit(request.POST, instance=poliza)
            form.save()
            messages.success(request, f'Registro editado!')
            return redirect('poliza')
        except ValueError:
            poliza = get_object_or_404(Polizas, pk=pk)
            form = PolizaFormEdit(instance=poliza)
            return render(request, 'soc/polizas/poliza_editar.html', {
                'form': form,
                'error': 'Error al editar poliza'
            })
@permission_required('mioc.delete_polizas')
def borrar_poliza(request, pk):
    poliza = get_object_or_404(Polizas, pk=pk)
    poliza.delete()
    messages.success(request, f'Poliza {poliza.empresa_poliza} eliminada!')
    return redirect('poliza')
@permission_required('mioc.view_polizas')
def lista_poliza(request):
    poliza = Polizas.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(poliza,5)
        poliza = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        poliza = Polizas.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__inspector__fullname__icontains=queryset) |
            Q(empresa_poliza__empresa__icontains=queryset) |
            Q(obervacion__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/polizas/poliza_lista.html', {'entity': poliza, 'paginator':paginator})

# Div. Carga de Certificados
@permission_required('mioc.view_certificados')
def lista_certificados(request):
    certificados = Certificados.objects.all().order_by('acta__obra__codObra','acta__acta')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(certificados,5)
        certificados = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        certificados = Certificados.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__inspector__fullname__icontains=queryset) |
            Q(nro_cert__icontains=queryset) |
            Q(periodo__icontains=queryset),
        ).distinct().order_by('acta__acta',)
    return render(request, 'soc/certificados/certificado_lista.html', {'entity': certificados, 'paginator':paginator})
@permission_required('mioc.view_certificados')
def lista_certificados_obra(request, obra_id):
    certificados = Certificados.objects.filter(acta__obra_id=obra_id).order_by('acta__acta')
    try:
        obra = certificados.values('acta__obra__institucion__name').annotate(cantidad=Sum('acta__acta'))
        obra = list(obra)
        obra = obra[0]['acta__obra__institucion__name'].title()
        queryset = request.GET.get('buscar')
        if queryset:
            certificados = certificados.filter(
                Q(obra__inspector__fullname__icontains=queryset) |
                Q(nro_cert__icontains=queryset) |
                Q(periodo__icontains=queryset),
            ).distinct().order_by('acta__acta',)
        if not certificados.exists():
            context = {
                'obra': obra,
                'modal': True,
                'modal_message': 'La obra aún no tiene certificados.',
            }
            return render(request, 'soc/certificados/certificado_lista_obra.html', context)
        return render(request, 'soc/certificados/certificado_lista_obra.html', {
            'certificados': certificados,
            'obra': obra
        })
    except ValidationError as e:
        error_message = e.messages[0]
        return render(request, 'soc/certificados/obras_lista.html', {'error': error_message})
    except Exception as e:
        return render(request, 'soc/certificados/obras_lista.html', {'error': 'Ocurrió un error inesperado.'})
@permission_required('mioc.add_certificados')
def crear_certificado(request):
    if request.method == 'GET':
        return render(request, 'soc/certificados/certificado_crear.html', {
            'form': CertificadoForm
        })
    else:
        form = CertificadoForm(request.POST)
        try:
            if form.is_valid():
                nuevo_cert = form.save(commit=False)
                nuevo_cert.cargaCert = request.user
                nuevo_cert.save()
                messages.success(request, f'Nuevo certificado creado')
                return redirect('certificados')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/certificados/certificado_crear.html', {'form': form, 'error': error_message})
        except Exception as e:
            return render(request, 'soc/certificados/certificado_crear.html', {'form': form, 'error': 'Ocurrió un error inesperado.'})
@permission_required('mioc.change_certificados')
def editar_certificado(request, pk):
    if request.method == 'GET':
        certif = get_object_or_404(Certificados, pk=pk)
        form = CertificadoForm(instance=certif)
        return render(request, 'soc/certificados/certificado_editar.html', {
            'form': form,
        })
    else:
        try:
            certif = get_object_or_404(Certificados, pk=pk)
            # Inicializar el formulario con valores originales
            initial_data = {
                'fecha': certif.acta.periodo,
                # 'fecha_acta': certif.fecha_acta,
            }
            form = CertificadoForm(request.POST, instance=certif, initial=initial_data)
            form.instance.ultimo_editor = request.user
            if form.is_valid():
                certif.ultima_modificacion = timezone.now()
                form.save()
                messages.success(request, f'Certificado {certif.nro_cert} editado!')
                return redirect('certificados')
            else:
                return render(request, 'soc/certificados/certificado_editar.html', {
                    'form': form,
                    'error': 'Error al editar certificado'
                })
        except ValueError:
            certif = get_object_or_404(Certificados, pk=pk)
            form = CertificadoForm(instance=certif)
            return render(request, 'soc/certificados/certificado_editar.html', {
                'form': form,
                'error': 'Error al editar certificado'
            })
@permission_required('mioc.delete_certificados')        
def borrar_certificado(request, pk):
    certificado = get_object_or_404(Certificados, pk=pk)
    certificado.delete()
    messages.success(request, f'Certificado {certificado.acta.acta} eliminado!')
    return redirect('certificados')
@permission_required('mioc.view_certificados')
def ver_certificado(request, pk):
    if request.method == 'GET':
        certif = get_object_or_404(Certificados, pk=pk)
        form = CertificadoViewForm(instance=certif)
        return render(request, 'soc/certificados/certificado_ver.html', {
            'form': form,
        })

def crear_actas_inicio(request):
    if request.method == 'GET':
        form = ActaInicioForm
        return render(request, 'soc/actas/actas_inicio_crear.html', {
            'form': form
        })
    else:
        form = ActaInicioForm(request.POST)
        try:
            if form.is_valid():
                dispo_inspector = form.save(commit=False)
                dispo_inspector.user = request.user
                dispo_inspector.save()
                messages.success(request, f'Nueva acta creada!')
                return redirect('inicio')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/actas/actas_inicio_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/actas/actas_inicio_crear.html')

def editar_actas_inicio(request, pk):
    acta = get_object_or_404(ActasInicio, pk=pk)
    if request.method == 'GET':
        form = ActaInicioFormEdit(instance=acta)
        return render(request, 'soc/actas/actas_inicio_editar.html', {
            'form': form
        })
    else:
        form = ActaInicioFormEdit(request.POST, instance=acta)
        try:
            if form.is_valid():
                dispo_inspector = form.save(commit=False)
                dispo_inspector.user = request.user
                dispo_inspector.save()
                messages.success(request, f'Acta {acta} editada!')
                return redirect('inicio')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/actas/actas_inicio_editar.html', {'form': form, 'error': error_message})

def borrar_actas_inicio(request, pk):
    acta = get_object_or_404(ActasInicio, pk=pk)
    acta.delete()
    messages.success(request, f'Acta {acta} eliminada!')
    return redirect('inicio')

def lista_actas_inicio(request):
    actas = ActasInicio.objects.all().order_by('-fecha')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(actas, 5)
        actas = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        actas = ActasInicio.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/actas/actas_inicio_lista.html', {'entity': actas, 'paginator': paginator })

def crear_certificado_AF(request):
    if request.method == 'GET':
        return render(request, 'soc/certificados/certificado_AF_crear.html', {
            'form': CertificadoAFForm
        })
    else:
        form = CertificadoAFForm(request.POST)
        try:
            if form.is_valid():
                nuevo_cert = form.save(commit=False)
                nuevo_cert.cargaCert = request.user
                nuevo_cert.save()
                messages.success(request, f'Nuevo certificado de Anticipo Financiero creado')
                return redirect('certificado_AF')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/certificados/certificado_AF_crear.html', {'form': form, 'error': error_message})
        except Exception as e:
            return render(request, 'soc/certificados/certificado_AF_crear.html', {'form': form, 'error': 'Ocurrió un error inesperado.'})

def editar_certificado_AF(request, pk):
    cert = get_object_or_404(CertificadosAF, pk=pk)
    if request.method == 'GET':
        form = CertificadoAFFormEdit(instance=cert)
        return render(request, 'soc/certificados/certificado_AF_editar.html', {
            'form': form
        })
    else:
        form = CertificadoAFFormEdit(request.POST, instance=cert)
        try:
            if form.is_valid():
                nuevo_cert = form.save(commit=False)
                nuevo_cert.cargaCert = request.user
                nuevo_cert.save()
                messages.success(request, f'Certificado de Anticipo Financiero editado')
                return redirect('certificado_AF')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/certificados/certificado_AF_editar.html', {'form': form, 'error': error_message})

def borrar_certificado_AF(request, pk):
    cert = get_object_or_404(CertificadosAF, pk=pk)
    cert.delete()
    messages.success(request, f'Certificado de Anticipo Financiero eliminado')
    return redirect('certificado_AF')

def lista_certificados_AF(request):
    cert = CertificadosAF.objects.all().order_by('-creado')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(cert, 5)
        cert = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        cert = CertificadosAF.objects.filter(
            Q(dispo__obra__institucion__name__icontains=queryset) |
            Q(dispo__obra__expedientes__icontains=queryset) |
            Q(expediente__icontains=queryset) |
            Q(cargaCert__username__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/certificados/certificado_AF_lista.html', {'entity': cert, 'paginator': paginator })
# Div Armado Expte. Pago
@permission_required('mioc.add_memorias')
def crear_memoria(request):
    if request.method == 'GET':
        form = MemoriaForm
        return render(request, 'soc/memorias/memoria_crear.html', {
            'form': form
        })
    else:
        form = MemoriaForm(request.POST)
        try:
            if form.is_valid():
                memoria = form.save(commit=False)
                memoria.user = request.user
                memoria.save()
                messages.success(request, f'Nueva memoria creada!')
                return redirect('memorias')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/memorias/memoria_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/memorias/memoria.html')
@permission_required('mioc.change_memorias')
def editar_memoria(request, pk):
    memoria = get_object_or_404(Memorias, pk=pk)
    if request.method == 'GET':
        form = MemoriaForm(instance=memoria)
        return render(request, 'soc/memorias/memoria_editar.html', {
            'form': form
        })
    else:
        try:
            memoria = get_object_or_404(Memorias, pk=pk)
            form = MemoriaForm(request.POST, instance=memoria)
            form.save()
            messages.success(request, f'Registro editado!')
            return redirect('memorias')
        except ValueError:
            memoria = get_object_or_404(Memorias, pk=pk)
            form = MemoriaForm(instance=memoria)
            return render(request, 'soc/memorias/memoria_editar.html', {
                'form': form,
                'error': 'Error al editar memoria'
            })
@permission_required('mioc.delete_memorias')
def borrar_memoria(request, pk):
    memoria = get_object_or_404(Memorias, pk=pk)
    memoria.delete()
    messages.success(request, f'Memoria {memoria.obra} eliminada!')
    return redirect('memorias')
@permission_required('mioc.view_memorias')
def lista_memoria(request):
    memoria = Memorias.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(memoria,5)
        memoria = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        memoria = Memorias.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__inspector__fullname__icontains=queryset) |
            Q(obra__empresa__icontains=queryset) |
            Q(obervacion__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/memorias/memoria_lista.html', {'entity': memoria, 'paginator':paginator})

def crear_factura_af(request):
    if request.method == 'GET':
        form = FacturasAFForm
        return render(request, 'soc/certificados/factura_AF_crear.html', {
            'form': form
        })
    else:
        form = FacturasAFForm(request.POST)
        try:
            if form.is_valid():
                cert = form.save(commit=False)
                cert.user = request.user
                cert.save()
                messages.success(request, f'Factura de Anticipo Financiero registrada!')
                return redirect('facturas_AF')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/certificados/factura_AF_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/certificados/factura_AF_lista.html')

def editar_factura_AF(request, pk):
    cert = get_object_or_404(facturasAF, pk=pk)
    if request.method == 'GET':
        form = FacturasAFFormEdit(instance=cert)
        return render(request, 'soc/certificados/factura_AF_editar.html', {
            'form': form
        })
    else:
        form = FacturasAFFormEdit(request.POST, instance=cert)
        try:
            form.save()
            messages.success(request, f'Registro editado!')
            return redirect('facturas_AF')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/certificados/factura_AF_editar.html', {'form': form, 'error': error_message})

def borrar_factura_AF(request, pk):
    cert = get_object_or_404(facturasAF, pk=pk)
    cert.delete()
    messages.success(request, f'Factura eliminada!')
    return redirect('facturas_AF')

def lista_factura_AF(request):
    cert = facturasAF.objects.all().order_by('-fecha')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(cert, 5)
        cert = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        cert = facturasAF.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__inspector__fullname__icontains=queryset) |
            Q(obra__empresa__icontains=queryset) |
            Q(obervacion__icontains=queryset),
        ).distinct().order_by('-fecha',)
    return render(request, 'soc/certificados/factura_AF_lista.html', {'entity': cert})

# Dpto Despacho SOC 
@permission_required('mioc.add_obras')
def crear_obra(request):
    if request.method == 'GET':
        form = ObraFormAll
        return render(request, 'soc/obras/obra_crear.html', {
            'form': form
        })
    else:
        form = ObraFormAll(request.POST)
        try:
            if form.is_valid():
                obra = form.save(commit=False)
                obra.user = request.user
                obra.save()
                messages.success(request, f'Nueva obra creada!')
                return redirect('obras')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/obra_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/obras/obras_lista.html')
@permission_required('mioc.change_obras')
def editar_obra(request, pk):
    obra = get_object_or_404(Obras, pk=pk)
    if request.method == 'GET':
        form = ObraFormAllEdit(instance=obra)
        return render(request, 'soc/obras/obra_editar.html', {
            'form': form
        })
    else:
        try:
            obra = get_object_or_404(Obras, pk=pk)
            form = ObraFormAllEdit(request.POST, instance=obra)
            form.save()
            messages.success(request, f'Registro editado!')
            return redirect('obras')
        except ValueError:
            obra = get_object_or_404(Obras, pk=pk)
            form = ObraFormAllEdit(instance=obra)
            return render(request, 'soc/obras/obra_editar.html', {
                'form': form,
                'error': 'Error al editar obra'
            })
@permission_required('mioc.view_obras')
def lista_obras(request):
    obras = Obras.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(obras,5)
        obras = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        obras = Obras.objects.filter(
            Q(expedientes__icontains=queryset) |
            Q(institucion__name__icontains=queryset) |
            Q(empresa__name__icontains=queryset),
        ).distinct().order_by('institucion',)
    return render(request, 'soc/obras/obras_lista.html', {'entity': obras, 'paginator':paginator })
@permission_required('mioc.view_obras')
def detalle_obra(request):
    obras = Obras.objects.all()
    memoria = Memorias.objects.filter(obra__in=obras)
    certificados = Certificados.objects.filter(acta__obra__in=obras).order_by('acta__acta')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(obras,10)
        obras = paginator.page(page)
    except:
        raise Http404
    context = {
        'memoria': memoria,
        'certificados': certificados,
        'entity': obras,
        'paginator':paginator
    }
    return render(request, 'soc/obras/obra_detalle.html', context)

def crear_anticipo(request):
    if request.method == 'GET':
        form = AntidipoFinancieroForm
        return render(request, 'soc/dispo/dispo_anticipo_crear.html', {
            'form': form
        })
    else:
        form = AntidipoFinancieroForm(request.POST)
        try:
            if form.is_valid():
                anticipo = form.save(commit=False)
                anticipo.user = request.user
                anticipo.save()
                messages.success(request, f'Nuevo anticipo creado!')
                return redirect('anticipo')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/dispo/dispo_anticipo_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/dispo/anticipo.html')

def editar_anticipo(request, pk):
    anticipo = get_object_or_404(AnticipoFinanciero, pk=pk)
    if request.method == 'GET':
        form = AntidipoFinancieroFormEdit(instance=anticipo)
        return render(request, 'soc/dispo/dispo_anticipo_editar.html', {
            'form': form
        })
    else:
        form = AntidipoFinancieroFormEdit(request.POST, instance=anticipo)
        form.save()
        messages.success(request, f'Registro editado!')
        return redirect('anticipo')

def borrar_anticipo(request, pk):
    anticipo = get_object_or_404(AnticipoFinanciero, pk=pk)
    anticipo.delete()
    messages.success(request, f'Registro eliminado!')
    return redirect('anticipo')

def lista_anticipo(request):
    anticipos = AnticipoFinanciero.objects.all()
    inspectores = DispoInspector.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(anticipos,5)
        anticipos = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        anticipos = AnticipoFinanciero.objects.filter(
            Q(obra__expedientes__icontains=queryset) |
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__empresa__name__icontains=queryset),
        ).distinct().order_by('obra__institucion',)
    return render(request, 'soc/dispo/dispo_anticipo_lista.html', {'entity': anticipos, 'paginator':paginator, 'inspectores':inspectores})

def crear_dispo_cert_af(request):
    if request.method == 'GET':
        form = DispoCertAFForm
        return render(request, 'soc/dispo/dispo_cert_af_crear.html', {
            'form': form
        })
    else:
        form = DispoCertAFForm(request.POST)
        try:
            if form.is_valid():
                dispo_cert_af = form.save(commit=False)
                dispo_cert_af.user = request.user
                dispo_cert_af.save()
                messages.success(request, f'Nueva disposicion creada!')
                return redirect('dispo_certificado_AF')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/dispo/dispo_cert_af_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/dispo/dispo_cert_af_lista.html')

def editar_dispo_cert_af(request, pk):
    dispo_cert_af = get_object_or_404(dispoCertAF, pk=pk)
    if request.method == 'GET':
        form = DispoCertAFFormEdit(instance=dispo_cert_af)
        return render(request, 'soc/dispo/dispo_cert_af_editar.html', {
            'form': form
        })
    else:
        form = DispoCertAFFormEdit(request.POST, instance=dispo_cert_af)
        form.save()
        messages.success(request, f'Registro editado!')
        return redirect('dispo_certificado_AF')

def borrar_dispo_cert_af(request, pk):
    dispo_cert_af = get_object_or_404(dispoCertAF, pk=pk)
    dispo_cert_af.delete()
    messages.success(request, f'Registro eliminado!')
    return redirect('dispo_certificado_AF')

def lista_dispo_cert_af(request):
    dispo_cert_af = dispoCertAF.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(dispo_cert_af,5)
        dispo_cert_af = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        dispo_cert_af = dispoCertAF.objects.filter(
            Q(dispo__icontains=queryset) |
            Q(certificado__dispo__obra__institucion__name__icontains=queryset) |
            Q(certificado__dispo__obra__empresa__name__icontains=queryset),
        ).distinct().order_by('-fecha',)

    return render(request, 'soc/dispo/dispo_cert_af_lista.html', {'entity': dispo_cert_af, 'paginator':paginator})

def crear_dispo_paralizacion(request):
    if request.method == 'GET':
        form = DispoParalizacionForm
        return render(request, 'soc/dispo/dispo_paral_crear.html', {
            'form': form
        })
    else:
        form = DispoParalizacionForm(request.POST)
        try:
            if form.is_valid():
                dispo_paral = form.save(commit=False)
                dispo_paral.user = request.user
                dispo_paral.save()
                messages.success(request, f'Nueva disposicion creada!')
                return redirect('dispo_paral')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/dispo/dispo_paral_crear.html', {'form': form, 'error': error_message})

def editar_dispo_paralizacion(request, pk):
    dispo_paral = get_object_or_404(DispoParalizacion, pk=pk)
    if request.method == 'GET':
        form = DispoParalizacionFormEdit(instance=dispo_paral)
        return render(request, 'soc/dispo/dispo_paral_editar.html', {
            'form': form
        })
    else:
        form = DispoParalizacionFormEdit(request.POST, instance=dispo_paral)
        form.save()
        messages.success(request, f'Registro editado!')
        return redirect('dispo_paral')

def borrar_dispo_paralizacion(request, pk):
    dispo_paral = get_object_or_404(DispoParalizacion, pk=pk)
    dispo_paral.delete()
    messages.success(request, f'Registro eliminado!')
    return redirect('dispo_paral')

def lista_dispo_paralizacion(request):
    dispo_paral = DispoParalizacion.objects.all().order_by('dispo_plan__obra__institucion__name','dispo_plan__nro_plan')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(dispo_paral,5)
        dispo_paral = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        dispo_paral = DispoParalizacion.objects.filter(
            Q(dispo__icontains=queryset) |
            Q(certificado__dispo__obra__institucion__name__icontains=queryset) |
            Q(certificado__dispo__obra__empresa__name__icontains=queryset),
        ).distinct().order_by('dispo_plan__obra__institucion__name','dispo_plan__nro_plan')
    return render(request, 'soc/dispo/dispo_paral_lista.html', {'entity': dispo_paral, 'paginator':paginator})

def crear_dispo_reinicio(request):
    if request.method == 'GET':
        form = DispoReinicioForm
        return render(request, 'soc/dispo/dispo_reinicio_crear.html', {
            'form': form
        })
    else:
        form = DispoReinicioForm(request.POST)
        try:
            if form.is_valid():
                dispo_reinicio = form.save(commit=False)
                dispo_reinicio.user = request.user
                dispo_reinicio.save()
                messages.success(request, f'Nueva disposicion creada!')
                return redirect('dispo_reinicio')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/dispo/dispo_reinicio_crear.html', {'form': form, 'error': error_message})

def editar_dispo_reinicio(request, pk):
    dispo_reinicio = get_object_or_404(DispoReinicio, pk=pk)
    if request.method == 'GET':
        form = DispoReinicioFormEdit(instance=dispo_reinicio)
        return render(request, 'soc/dispo/dispo_reinicio_editar.html', {
            'form': form
        })
    else:
        form = DispoReinicioFormEdit(request.POST, instance=dispo_reinicio)
        form.save()
        messages.success(request, f'Registro editado!')
        return redirect('dispo_reinicio')

def borrar_dispo_reinicio(request, pk):
    dispo_reinicio = get_object_or_404(DispoReinicio, pk=pk)
    dispo_reinicio.delete()
    messages.success(request, f'Registro eliminado!')
    return redirect('dispo_reinicio')

def lista_dispo_reinicio(request):
    dispo_reinicio = DispoReinicio.objects.all().order_by('dispo_para__dispo_plan__obra__institucion__name','dispo_para__dispo_plan__nro_plan')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(dispo_reinicio,5)
        dispo_reinicio = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        dispo_reinicio = DispoReinicio.objects.filter(
            Q(dispo__icontains=queryset) |
            Q(certificado__dispo__obra__institucion__name__icontains=queryset) |
            Q(certificado__dispo__obra__empresa__name__icontains=queryset),
        ).distinct().order_by('dispo_para__dispo_plan__obra__institucion__name','dispo_para__dispo_plan__nro_plan')
    return render(request, 'soc/dispo/dispo_reinicio_lista.html', {'entity': dispo_reinicio, 'paginator':paginator})


# Dpto. Despacho DPO 
@permission_required('mioc.add_dispoinspector')
def crear_dispo_inspector(request):
    if request.method == 'GET':
        form = DispoInspForm
        return render(request, 'soc/dispo/dispo_inspector_crear.html', {
            'form': form
        })
    else:
        form = DispoInspForm(request.POST)
        try:
            if form.is_valid():
                dispo_inspector = form.save(commit=False)
                dispo_inspector.user = request.user
                dispo_inspector.save()
                messages.success(request, f'Nueva disposicion creada!')
                return redirect('dispo_inspe')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/dispo/dispo_inspector_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/dispo/dispo_inspector_lista.html')
@permission_required('mioc.change_dispoinspector')
def editar_dispo_inspector(request, pk):
    obra = get_object_or_404(DispoInspector, pk=pk)
    if request.method == 'GET':
        form = DispoInspFormEdit(instance=obra)
        return render(request, 'soc/dispo/dispo_inspector_editar.html', {
            'form': form
        })
    else:
        try:
            obra = get_object_or_404(DispoInspector, pk=pk)
            form = DispoInspFormEdit(request.POST, instance=obra)
            form.save()
            messages.success(request, f'Registro editado!')
            return redirect('dispo_inspe')
        except ValueError:
            obra = get_object_or_404(DispoInspector, pk=pk)
            form = DispoInspFormEdit(instance=obra)
            return render(request, 'soc/dispo/dispo_inspector_editar.html', {
                'form': form,
                'error': 'Error al editar disposicion'
            })
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/dispo/dispo_inspector_editar.html', {'form': form, 'error': error_message})
@permission_required('mioc.delete_dispoinspector')
def borrar_dispo_inspector(request, pk):
    dispo = get_object_or_404(DispoInspector, pk=pk)
    dispo.delete()
    messages.success(request, f'Registro eliminado!')
    return redirect('dispo_inspe')
@permission_required('mioc.view_dispoinspector')
def lista_dispo_inspector(request):
    poliza = DispoInspector.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(poliza,5)
        poliza = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        poliza = DispoInspector.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(inspector__fullname__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(dispo__icontains=queryset) |
            Q(fecha__icontains=queryset)|
            Q(observacion__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/dispo/dispo_inspector_lista.html', {'entity': poliza, 'paginator':paginator})
@permission_required('mioc.view_dispoinspector')
def lista_dispo_inspector_obra(request, obra_id):
    disposicion = DispoInspector.objects.filter(obra_id=obra_id).order_by('fecha')
    try:
        obra = disposicion.values('obra__institucion__name').annotate(cantidad=Sum('id'))
        obra = list(obra)
        obra = obra[0]['obra__institucion__name'].title()
        queryset = request.GET.get('buscar')
        if queryset:
            disposicion = disposicion.filter(
                Q(obra__institucion__name__icontains=queryset) |
                Q(inspector__fullname__icontains=queryset) |
                Q(dispo__icontains=queryset) |
                Q(fecha__icontains=queryset)|
                Q(observacion__icontains=queryset),
            ).distinct().order_by('id',)
        if not disposicion.exists():
            context = {
                'obra': obra,
                'modal': True,
                'modal_message': 'La obra no tiene disposiciones',
            }
            return render(request, 'soc/dispo/dispo_inspector_lista_obra.html', context)
        return render(request, 'soc/dispo/dispo_inspector_lista_obra.html', {
            'dispo': disposicion,
            'obra': obra
        })
    except ValidationError as e:
        error_message = e.messages[0]
        return render(request, 'soc/dispo/dispo_inspector_lista.html', {'error': error_message})
    except Exception as e:
        return render(request, 'soc/dispo/dispo_inspector_lista.html', {'error': 'Ocurrio un error inesperado.'})

# Inspección de Obras

def crear_actas_obras(request):
    if request.method == 'GET':
        form = ActaMedicionForm
        return render(request, 'soc/medicion/actas_obras_crear.html', {
            'form': form
        })
    else:
        form = ActaMedicionForm(request.POST)
        try:
            if form.is_valid():
                dispo_inspector = form.save(commit=False)
                dispo_inspector.user = request.user
                if dispo_inspector.acta == 0:
                    dispo_inspector.acta = 1
                dispo_inspector.save()
                messages.success(request, f'Nueva disposicion creada!')
                return redirect('medicion')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/medicion/actas_obras_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/medicion/actas_obras_crear.html')

def editar_actas_obras(request, pk):
    acta = get_object_or_404(ActaMedicion, pk=pk)
    if request.method == 'GET':
        form = ActaMedicionFormEdit(instance=acta)
        return render(request, 'soc/medicion/actas_obras_editar.html', {
            'form': form
        })
    else:
        form = ActaMedicionFormEdit(request.POST, instance=acta)
        try:
            if form.is_valid():
                dispo_inspector = form.save(commit=False)
                dispo_inspector.user = request.user
                dispo_inspector.save()
                messages.success(request, f'Medición {acta} editada!')
                return redirect('medicion')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/medicion/actas_obras_editar.html', {'form': form, 'error': error_message})

def borrar_actas_obras(request, pk):
    acta = get_object_or_404(ActaMedicion, pk=pk)
    acta.delete()
    messages.success(request, f'Medición {acta} eliminada!')
    return redirect('medicion')

def lista_actas_obras(request):
    actas = ActaMedicion.objects.all().order_by('obra__institucion__name','-acta')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(actas, 5)
        actas = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        actas = ActaMedicion.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(acta_nro__icontains=queryset) |
            Q(periodo__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/medicion/actas_obras_lista.html', {'entity': actas, 'paginator': paginator })

# Dpto. Certificaciones

def crear_estructura(request):
    if request.method == 'GET':
        form = EstructuraForm
        return render(request, 'soc/obras/obra_estructura_crear.html', {
            'form': form
        })
    else:
        form = EstructuraForm(request.POST)
        try:
            if form.is_valid():
                dispo_inspector = form.save(commit=False)
                dispo_inspector.user = request.user
                dispo_inspector.save()
                messages.success(request, f'Nueva estructura informada!')
                return redirect('estructuras')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/obra_estructura_crear.html', {'form': form, 'error': error_message})
    return render(request, 'soc/obras/obra_estructura_crear.html')

def editar_estructura(request, pk):
    estructura = get_object_or_404(Estructuras, pk=pk)
    if request.method == 'GET':
        form = EstructuraFormEdit(instance=estructura)
        return render(request, 'soc/obras/obra_estructura_editar.html', {
            'form': form
        })
    else:
        form = EstructuraFormEdit(request.POST, instance=estructura)
        try:
            if form.is_valid():
                dispo_inspector = form.save(commit=False)
                dispo_inspector.user = request.user
                dispo_inspector.save()
                messages.success(request, f'Estructura {estructura} editada!')
                return redirect('estructuras')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/obra_estructura_editar.html', {'form': form, 'error': error_message})

def borrar_estructura(request, pk):
    estructura = get_object_or_404(Estructuras, pk=pk)
    estructura.delete()
    messages.success(request, f'Estructura {estructura} eliminada!')
    return redirect('estructuras')

def lista_estructura(request):
    estructuras = Estructuras.objects.all().order_by('-fecha')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(estructuras, 5)
        estructuras = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        estructuras = Estructuras.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__empresa__name__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(link__icontains=queryset) |
            Q(fecha__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/obras/obra_estructura_lista.html', {'entity': estructuras, 'paginator': paginator })

def lista_estructura_inspector(request):
    estructuras = Estructuras.objects.filter(inspector__user=request.user.pk).order_by('-fecha')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(estructuras, 5)
        estructuras = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        estructuras = Estructuras.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__empresa__name__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(link__icontains=queryset) |
            Q(fecha__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'soc/obras/obra_estructura_lista_inspector.html', {'entity': estructuras, 'paginator': paginator })

def validar_acta(request):
    if request.method == 'GET':
        form = ActaMedicionValidatedForm
        return render(request, 'soc/medicion/actas_obras_validar.html', {
            'form': form
        })
    else:
        form = ActaMedicionValidatedForm(request.POST)
        try:
            if form.is_valid():
                validated = form.save(commit=False)
                validated.user = request.user
                validated.save()
                messages.success(request, f'Acta {validated} validada!')
                return redirect('lista_validar_acta')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/medicion/actas_obras_validar.html', {'form': form, 'error': error_message})

def editar_validar_acta(request, pk):
    acta = get_object_or_404(ActaMedicionValidacion, pk=pk)
    if request.method == 'GET':
        form = ActaMedicionValidatedFormEdit(instance=acta)
        return render(request, 'soc/medicion/actas_obras_validar_editar.html', {
            'form': form
        })
    else:
        form = ActaMedicionValidatedFormEdit(request.POST, instance=acta)
        try:
            if form.is_valid():
                validated = form.save(commit=False)
                validated.user = request.user
                validated.save()
                messages.success(request, f'Acta {validated} validada!')
                return redirect('lista_validar_acta')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/medicion/actas_obras_validar_editar.html', {'form': form, 'error': error_message})

def borrar_validar_acta(request, pk):
    acta = get_object_or_404(ActaMedicionValidacion, pk=pk)
    acta.delete()
    messages.success(request, f'Acta {acta} eliminada!')
    return redirect('lista_validar_acta')

def lista_validar_acta(request):
    actas = ActaMedicionValidacion.objects.all().order_by('-acta')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(actas, 5)
        actas = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        actas = ActaMedicionValidacion.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__empresa__name__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(link__icontains=queryset) |
            Q(fecha__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('acta',)
    return render(request, 'soc/medicion/actas_obras_validar_lista.html', {'entity': actas })

def crear_dispo_plan_trabajo(request):
    if request.method == 'GET':
        form = dispo_plan_trabajoForm
        return render(request, 'soc/obras/dispo_plan_trabajo_crear.html', {
            'form': form
        })
    else:
        form = dispo_plan_trabajoForm(request.POST)
        try:
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = request.user
                plan.save()
                messages.success(request, f'Plan de trabajo creado!')
                return redirect('lista_dispo_plan_trabajo')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/dispo_plan_trabajo_crear.html', {'form': form, 'error': error_message})

def crear_dispo_plan_trabajo_2(request):
    if request.method == 'GET':
        form = dispo_plan_trabajo_2Form
        return render(request, 'soc/obras/dispo_plan_trabajo_crear_2.html', {
            'form': form
        })
    else:
        form = dispo_plan_trabajo_2Form(request.POST)
        try:
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = request.user
                plan.save()
                messages.success(request, f'Plan de trabajo creado!')
                return redirect('lista_dispo_plan_trabajo_2')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/dispo_plan_trabajo_crear_2.html', {'form': form, 'error': error_message})
        
def editar_dispo_plan_trabajo(request, pk):
    plan = get_object_or_404(dispo_plan_trabajo, pk=pk)
    if request.method == 'GET':
        form = dispo_plan_trabajoFormEdit(instance=plan)
        return render(request, 'soc/obras/dispo_plan_trabajo_editar.html', {
            'form': form
        })
    else:
        form = dispo_plan_trabajoFormEdit(request.POST, instance=plan)
        try:
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = request.user
                plan.save()
                messages.success(request, f'Plan de trabajo editado!')
                return redirect('lista_dispo_plan_trabajo')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/dispo_plan_trabajo_editar.html', {'form': form, 'error': error_message})

def editar_dispo_plan_trabajo_2(request, pk):
    plan = get_object_or_404(dispo_plan_trabajo, pk=pk)
    if request.method == 'GET':
        form = dispo_plan_trabajoFormEdit(instance=plan)
        return render(request, 'soc/obras/dispo_plan_trabajo_editar_2.html', {
            'form': form
        })
    else:
        form = dispo_plan_trabajoFormEdit(request.POST, instance=plan)
        try:
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = request.user
                plan.save()
                messages.success(request, f'Plan de trabajo editado!')
                return redirect('lista_dispo_plan_trabajo_2')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/dispo_plan_trabajo_editar_2.html', {'form': form, 'error': error_message})

def borrar_dispo_plan_trabajo(request, pk):
    plan = get_object_or_404(dispo_plan_trabajo, pk=pk)
    plan.delete()
    messages.success(request, f'Plan de trabajo eliminado!')
    return redirect('lista_dispo_plan_trabajo')

def borrar_dispo_plan_trabajo_2(request, pk):
    plan = get_object_or_404(dispo_plan_trabajo, pk=pk)
    plan.delete()
    messages.success(request, f'Plan de trabajo eliminado!')
    return redirect('lista_dispo_plan_trabajo_2')

def lista_dispo_plan_trabajo(request):
    plans = dispo_plan_trabajo.objects.filter(tipo='0').order_by('-obra')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(plans, 5)
        plans = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        plans = dispo_plan_trabajo.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__empresa__name__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(instrumento__icontains=queryset) |
            Q(fecha_aplicacion__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('obra',)
    return render(request, 'soc/obras/dispo_plan_trabajo_lista.html', {'entity': plans })

def lista_dispo_plan_trabajo_2(request):
    plans = dispo_plan_trabajo.objects.filter(tipo='1').order_by('obra','nro_plan')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(plans, 5)
        plans = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        plans = dispo_plan_trabajo.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__empresa__name__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(instrumento__icontains=queryset) |
            Q(fecha_aplicacion__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('obra','nro_plan')
    return render(request, 'soc/obras/dispo_plan_trabajo_lista_2.html', {'entity': plans })

def crear_plan_trabajo(request):
    if request.method == 'GET':
        form = PlanTrabajoForm()
        return render(request, 'soc/obras/plan_trabajo_crear.html', {
            'form': form
        })
    else:
        form = PlanTrabajoForm(request.POST)
        try:
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = request.user
                plan.save()
                messages.success(request, f'Plan de trabajo creado!')
                return redirect('lista_plan_trabajo')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/plan_trabajo_crear.html', {'form': form, 'error': error_message})

def editar_plan_trabajo(request, pk):
    plan = get_object_or_404(PlanTrabajo, pk=pk)
    if request.method == 'GET':
        form = PlanTrabajoForm(instance=plan)
        return render(request, 'soc/obras/plan_trabajo_editar.html', {
            'form': form
        })
    else:
        form = PlanTrabajoForm(request.POST, instance=plan)
        try:
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = request.user
                plan.save()
                messages.success(request, f'Plan de trabajo editado!')
                return redirect('lista_plan_trabajo')
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'soc/obras/plan_trabajo_editar.html', {'form': form, 'error': error_message})

def borrar_plan_trabajo(request, pk):
    plan = get_object_or_404(PlanTrabajo, pk=pk)
    plan.delete()
    messages.success(request, f'Plan de trabajo eliminado!')
    return redirect('lista_plan_trabajo')

def lista_plan_trabajo(request):
    plans = PlanTrabajo.objects.all().order_by('dispo_plan','periodoNro')
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(plans, 5)
        plans = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        plans = dispo_plan_trabajo.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__empresa__name__icontains=queryset) |
            Q(obra__expedientes__icontains=queryset) |
            Q(instrumento__icontains=queryset) |
            Q(fecha_aplicacion__icontains=queryset) |
            Q(user__username__icontains=queryset),
        ).distinct().order_by('dispo_plan','periodoNro')
    return render(request, 'soc/obras/plan_trabajo_lista.html', {'entity': plans })
