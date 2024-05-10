from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q,Sum
from django.contrib.auth.decorators import  permission_required
from django.core.paginator import Paginator
from django.contrib import messages
from . models import ActasObras, Certificados, Obras, EmpresaPoliza
from . forms import ActasObrasFormEdit, CertificadoForm, CertificadoFormEdit, ObraFormAll, ObraFormActas, EmpresaPolizaForm, ActasObrasForm


# Create your views here.


def index(request):
    saludo = 'Portal de Pedidos'
    creador = 'Lucas L.'
    return render(request, 'index.html', {
        'titulo': saludo,
        'creador': creador,
    })
# @permission_required('mioc.view_uvis')

def obras(request):
    obras = Obras.objects.all()
    queryset = request.GET.get('buscar')
    if queryset:
        obras = Obras.objects.filter(
            Q(expedientes__icontains=queryset) |
            Q(institucion__name__icontains=queryset) |
            Q(inspector__fullname__icontains=queryset) |
            Q(empresa__name__icontains=queryset),
        ).distinct().order_by('institucion',)
    return render(request, 'obras.html', {'obras': obras, })

def obra_detalle(request, pk):
    if request.method == 'GET':
        pedido = get_object_or_404(Obras, pk=pk)
        form = ObraFormAll(instance=pedido)
        form2 = ObraFormActas(instance=pedido)
        return render(request, 'obra_detalle.html', {
            'form': form,
            'form2': form2,
        })
    else:
        try:
            pedido = get_object_or_404(Obras, pk=pk)
            form2 = ObraFormActas(request.POST, instance=pedido)
            form2.save()
            return redirect(f'/obras/detalle/{pk}/')
        except ValueError:
            pedido = get_object_or_404(Obras, pk=pk)
            form = ObraFormAll(instance=pedido)
            return render(request, 'obra_detalle.html', {
                'form': form,
                'error': 'Error al validar pedido.'
            })

def obra_poliza(request, pk):
    if request.method == 'GET':
        pedido = get_object_or_404(Obras, pk=pk)
        form = ObraFormAll(instance=pedido)
        form2 = ObraFormActas(instance=pedido)
        return render(request, 'obra_poliza.html', {
            'form': form,
            'form2': form2,
        })
    else:
        try:
            pedido = get_object_or_404(Obras, pk=pk)
            form2 = ObraFormActas(request.POST, instance=pedido)
            form2.save()
            messages.success(request, f'Poliza de {pedido.institucion} validada!')
            return redirect(f'/obras/poliza/{pk}/')
        except ValueError:
            pedido = get_object_or_404(Obras, pk=pk)
            form = ObraFormAll(instance=pedido)
            return render(request, 'obra_poliza.html', {
                'form': form,
                'error': 'Error al validar pedido.'
            })

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

def certificados_lista(request):
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

def certificados_lista_obra(request, obra_id):
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
        return render(request, 'obras.html', {'error': error_message})
    except Exception as e:
        return render(request, 'obras.html', {'error': 'Ocurrió un error inesperado.'})

def create_certificado(request):
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

def edit_certificado(request, pk):
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
        
def delete_certificado(request, pk):
    certificado = get_object_or_404(Certificados, pk=pk)
    certificado.delete()
    messages.success(request, f'Certificado {certificado.nro_cert} eliminado!')
    return redirect('certificados')

def actas_lista(request):
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

def actas_lista_obras(request,obra_id):
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

def actas_obras(request):
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

def actas_obras_editar(request, pk):
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