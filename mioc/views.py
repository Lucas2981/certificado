from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q,Sum
from django.contrib.auth.decorators import  permission_required
from django.core.paginator import Paginator
from django.contrib import messages
from . models import ActasObras, Certificados, DispoInspector, Memorias, Obras, EmpresaPoliza, Polizas
from . forms import ActasObrasFormEdit, CertificadoForm, CertificadoFormEdit, DispoInspForm, DispoInspFormEdit, MemoriaForm, ObraFormAll, ObraFormActas, EmpresaPolizaForm, ActasObrasForm, PolizaForm


# Create your views here.


def index(request):
    saludo = 'Portal de Pedidos'
    creador = 'Lucas L.'
    return render(request, 'index.html', {
        'titulo': saludo,
        'creador': creador,
    })

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
            Q(inspector__fullname__icontains=queryset) |
            Q(empresa__name__icontains=queryset),
        ).distinct().order_by('institucion',)
    return render(request, 'obras_lista.html', {'entity': obras, 'paginator':paginator })

def detalle_obra(request):
    obras = Obras.objects.all()
    memoria = Memorias.objects.filter(obra__in=obras)
    certificados = Certificados.objects.filter(obra__in=obras)
    context = {
        'memoria':memoria,
        'certificados':certificados,
        'obras':obras
    }
    return render(request, 'obra_detalle.html', context)

def create_empresa(request):
    if request.method == 'GET':
        return render(request, 'fondo_reparo_crear.html', {
            'form': EmpresaPolizaForm
        })
    else:
        form = EmpresaPolizaForm(request.POST)
        if form.is_valid():
            nueva_empresa = form.save(commit=False)
            nueva_empresa.creaEmpresa = request.user
            nueva_empresa.save()
            messages.success(request, f'Nueva empresa creada!')
            return redirect('aseguradora')

def edit_empresa(request, pk):
    if request.method == 'GET':
        asegura = get_object_or_404(EmpresaPoliza, pk=pk)
        form = EmpresaPolizaForm(instance=asegura)
        return render(request, 'fondo_reparo_editar.html', {
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
            return render(request, 'fondo_reparo_editar.html', {
                'form': form,
                'error': 'Error al validar pedido.'
            })

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
    return render(request, 'empresa_lista.html', {'entity': empresa, 'paginator':paginator })

def lista_certificados(request):
    certificados = Certificados.objects.all()
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
        ).distinct().order_by('nro_cert',)
    return render(request, 'certificado_lista.html', {'entity': certificados, 'paginator':paginator})

def lista_certificados_obra(request, obra_id):
    certificados = Certificados.objects.filter(obra_id=obra_id).order_by('nro_cert')
    try:
        obra = certificados.values('obra__institucion__name').annotate(cantidad=Sum('nro_cert'))
        obra = list(obra)
        obra = obra[0]['obra__institucion__name'].title()
        queryset = request.GET.get('buscar')
        if queryset:
            certificados = certificados.filter(
                Q(obra__inspector__fullname__icontains=queryset) |
                Q(nro_cert__icontains=queryset) |
                Q(periodo__icontains=queryset),
            ).distinct().order_by('nro_cert',)
        if not certificados.exists():
            context = {
                'obra': obra,
                'modal': True,
                'modal_message': 'La obra aún no tiene certificados.',
            }
            return render(request, 'certificado_lista_obra.html', context)
        return render(request, 'certificado_lista_obra.html', {
            'certificados': certificados,
            'obra': obra
        })
    except ValidationError as e:
        error_message = e.messages[0]
        return render(request, 'obras_lista.html', {'error': error_message})
    except Exception as e:
        return render(request, 'obras_lista.html', {'error': 'Ocurrió un error inesperado.'})

def crear_certificado(request):
    if request.method == 'GET':
        return render(request, 'certificado_crear.html', {
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
            # Handle the ValidationError raised by the model's clean method
            error_message = e.messages[0]  # Get the first error message
            return render(request, 'certificado_crear.html', {'form': form, 'error': error_message})
        except Exception as e:
            # Handle any other exceptions that may occur
            return render(request, 'certificado_crear.html', {'form': form, 'error': 'Ocurrió un error inesperado.'})

def editar_certificado(request, pk):
    if request.method == 'GET':
        certif = get_object_or_404(Certificados, pk=pk)
        form = CertificadoFormEdit(instance=certif)
        return render(request, 'certificado_editar.html', {
            'form': form,
        })
    else:
        try:
            certif = get_object_or_404(Certificados, pk=pk)
            # Inicializar el formulario con valores originales
            initial_data = {
                'fecha': certif.fecha,
                'fecha_acta': certif.fecha_acta,
            }
            form = CertificadoFormEdit(request.POST, instance=certif, initial=initial_data)
            form.save()
            messages.success(request, f'Certificado {certif.nro_cert} editado!')
            return redirect('certificados')
        except ValueError:
            certif = get_object_or_404(Certificados, pk=pk)
            form = CertificadoFormEdit(instance=certif)
            return render(request, 'certificado_editar.html', {
                'form': form,
                'error': 'Error al editar certificado'
            })
        
def borrar_certificado(request, pk):
    certificado = get_object_or_404(Certificados, pk=pk)
    certificado.delete()
    messages.success(request, f'Certificado {certificado.nro_cert} eliminado!')
    return redirect('certificados')

def lista_actas(request):
    actas = ActasObras.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(actas,5)
        actas = paginator.page(page)
    except:
        raise Http404
    queryset = request.GET.get('buscar')
    if queryset:
        actas = ActasObras.objects.filter(
            Q(obra__institucion__name__icontains=queryset) |
            Q(obra__inspector__fullname__icontains=queryset) |
            Q(nro_cert__icontains=queryset) |
            Q(periodo__icontains=queryset),
        ).distinct().order_by('nro_cert',)
    return render(request, 'actas_lista.html', {'entity': actas, 'paginator':paginator})

def lista_actas_obra(request,obra_id):
    actas = ActasObras.objects.filter(obra_id=obra_id).order_by('obra__institucion__name')
    try:
        obra = actas.values('obra__institucion__name').annotate(cantidad=Sum('id'))
        obra = list(obra)
        obra = obra[0]['obra__institucion__name'].title()
        queryset = request.GET.get('buscar')
        if queryset:
            actas = actas.filter(
                Q(obra__inspector__fullname__icontains=queryset) |
                Q(nro_cert__icontains=queryset) |
                Q(periodo__icontains=queryset),
            ).distinct().order_by('nro_cert',)
        if not actas.exists():
            context = {
                'obra': obra,
                'modal': True,
                'modal_message': 'La obra aún no tiene actas.',
            }
            return render(request, 'actas_lista_obra.html', context)
        return render(request, 'actas_lista_obra.html', {
            'actas': actas,
            'obra': obra
        })
    except ValidationError as e:
        error_message = e.messages[0]
        return render(request, 'actas.html', {'error': error_message})
    except Exception as e:
        return render(request, 'actas.html', {'error': 'Ocurrió un error inesperado.'})

def crear_acta(request):
    if request.method == 'GET':
        return render(request, 'actas_obras.html', {
            'form': ActasObrasForm
        })
    else:
        form = ActasObrasForm(request.POST)
        try:
            if form.is_valid():
                nueva_acta = form.save(commit=False)
                nueva_acta.cargaCert = request.user
                nueva_acta.save()
                messages.success(request, f'Nuevo acta creada')
                return redirect('actas')
        except ValidationError as e:
            # Handle the ValidationError raised by the model's clean method
            error_message = e.messages[0]  # Get the first error message
            return render(request, 'actas_obras.html', {'form': form, 'error': error_message})
        except Exception as e:
            # Handle any other exceptions that may occur
            return render(request, 'actas_obras.html', {'form': form, 'error': 'Ocurrió un error inesperado.'})
    return render(request, 'actas_obras.html')

def editar_acta(request, pk):
    acta = get_object_or_404(ActasObras, pk=pk)
    if request.method == 'GET':
        form = ActasObrasFormEdit(instance=acta)
        return render(request, 'actas_obras_editar.html', {
            'form': form
        })
    else:
        try:
            acta = get_object_or_404(ActasObras, pk=pk)
            form = ActasObrasFormEdit(request.POST, instance=acta)
            form.save()
            messages.success(request, f'Acta de {acta.tipo} editada!')
            return redirect('actas')
        except ValueError:
            acta = get_object_or_404(ActasObras, pk=pk)
            form = ActasObrasFormEdit(instance=acta)
            return render(request, 'actas_obras_editar.html', {
                'form': form,
                'error': 'Error al editar acta'
            })

def crear_poliza(request):
    if request.method == 'GET':
        form = PolizaForm
        return render(request, 'poliza_crear.html', {
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
            return render(request, 'poliza_crear.html', {'form': form, 'error': error_message})

def editar_poliza(request, pk):
    poliza = get_object_or_404(Polizas, pk=pk)
    if request.method == 'GET':
        form = PolizaForm(instance=poliza)
        return render(request, 'poliza_editar.html', {
            'form': form
        })
    else:
        try:
            poliza = get_object_or_404(Polizas, pk=pk)
            form = PolizaForm(request.POST, instance=poliza)
            form.save()
            messages.success(request, f'Registro editado!')
            return redirect('poliza')
        except ValueError:
            poliza = get_object_or_404(Polizas, pk=pk)
            form = PolizaForm(instance=poliza)
            return render(request, 'poliza_editar.html', {
                'form': form,
                'error': 'Error al editar poliza'
            })

def borrar_poliza(request, pk):
    poliza = get_object_or_404(Polizas, pk=pk)
    poliza.delete()
    messages.success(request, f'Poliza {poliza.empresa_poliza} eliminada!')
    return redirect('poliza')

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
    return render(request, 'poliza_lista.html', {'entity': poliza, 'paginator':paginator})

def crear_memoria(request):
    if request.method == 'GET':
        form = MemoriaForm
        return render(request, 'poliza_crear.html', {
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
            return render(request, 'memoria_crear.html', {'form': form, 'error': error_message})
    return render(request, 'memoria.html')

def editar_memoria(request, pk):
    memoria = get_object_or_404(Memorias, pk=pk)
    if request.method == 'GET':
        form = MemoriaForm(instance=memoria)
        return render(request, 'memoria_editar.html', {
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
            return render(request, 'memoria_editar.html', {
                'form': form,
                'error': 'Error al editar memoria'
            })

def borrar_memoria(request, pk):
    memoria = get_object_or_404(Memorias, pk=pk)
    memoria.delete()
    messages.success(request, f'Memoria {memoria.obra} eliminada!')
    return redirect('memorias')

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
    return render(request, 'memoria_lista.html', {'entity': memoria, 'paginator':paginator})

def crear_obra(request):
    if request.method == 'GET':
        form = ObraFormAll
        return render(request, 'obra_crear.html', {
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
            return render(request, 'obra_crear.html', {'form': form, 'error': error_message})
    return render(request, 'obra.html')

def editar_obra(request, pk):
    obra = get_object_or_404(Obras, pk=pk)
    if request.method == 'GET':
        form = ObraFormAll(instance=obra)
        return render(request, 'obra_editar.html', {
            'form': form
        })
    else:
        try:
            obra = get_object_or_404(Obras, pk=pk)
            form = ObraFormAll(request.POST, instance=obra)
            form.save()
            messages.success(request, f'Registro editado!')
            return redirect('obras')
        except ValueError:
            obra = get_object_or_404(Obras, pk=pk)
            form = ObraFormAll(instance=obra)
            return render(request, 'obra_editar.html', {
                'form': form,
                'error': 'Error al editar obra'
            })

def crear_dispo_inspector(request):
    if request.method == 'GET':
        form = DispoInspForm
        return render(request, 'dispo_inspector_crear.html', {
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
            return render(request, 'dispo_inspector_crear.html', {'form': form, 'error': error_message})
    return render(request, 'dispo_inspector_lista.html')

def editar_dispo_inspector(request, pk):
    obra = get_object_or_404(DispoInspector, pk=pk)
    if request.method == 'GET':
        form = DispoInspFormEdit(instance=obra)
        return render(request, 'dispo_inspector_editar.html', {
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
            return render(request, 'dispo_inspector_editar.html', {
                'form': form,
                'error': 'Error al editar disposicion'
            })
        except ValidationError as e:
            error_message = e.messages[0]
            return render(request, 'dispo_inspector_editar.html', {'form': form, 'error': error_message})

def borrar_dispo_inspector(request, pk):
    dispo = get_object_or_404(DispoInspector, pk=pk)
    dispo.delete()
    messages.success(request, f'Registro eliminado!')
    return redirect('dispo_inspe')
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
            Q(dispo__icontains=queryset) |
            Q(fecha__icontains=queryset)|
            Q(observacion__icontains=queryset),
        ).distinct().order_by('id',)
    return render(request, 'dispo_inspector_lista.html', {'entity': poliza, 'paginator':paginator})

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
            return render(request, 'dispo_inspector_lista_obra.html', context)
        return render(request, 'dispo_inspector_lista_obra.html', {
            'dispo': disposicion,
            'obra': obra
        })
    except ValidationError as e:
        error_message = e.messages[0]
        return render(request, 'dispo_inspector_lista.html', {'error': error_message})
    except Exception as e:
        return render(request, 'dispo_inspector_lista.html', {'error': 'Ocurrio un error inesperado.'})
