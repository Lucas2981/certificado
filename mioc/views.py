from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q,Sum
from . models import Certificados, Obras, EmpresaPoliza
from . forms import CertificadoForm, ObraFormAll, ObraFormActas, EmpresaPolizaForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


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
    queryset = request.GET.get('buscar')
    if queryset:
        empresa = EmpresaPoliza.objects.filter(
            Q(empresa__icontains=queryset) |
            Q(location__icontains=queryset) |
            Q(telefono__icontains=queryset),
        ).distinct().order_by('empresa',)
    return render(request, 'empresa_lista.html', {'empresa': empresa, })

def certificados_lista(request):
    certificados = Certificados.objects.all()
    queryset = request.GET.get('buscar')
    if queryset:
        certificados = Certificados.objects.filter(
            Q(obra__icontains=queryset) |
            Q(nro_cert__name__icontains=queryset) |
            Q(fecha__fullname__icontains=queryset) |
            Q(uvi__name__icontains=queryset),
        ).distinct().order_by('nro_cert',)
    return render(request, 'certificado_lista.html', {'certificados': certificados, })


def certificados_lista_obra(request, obra_id):
    certificados = Certificados.objects.filter(obra_id=obra_id).order_by('nro_cert')
    obra = certificados.values('obra__institucion__name').annotate(cantidad=Sum('nro_cert'))
    obra = list(obra)
    obra = obra[0]['obra__institucion__name'].title()
    queryset = request.GET.get('buscar')
    if queryset:
        certificados = Certificados.objects.filter(
            Q(nro_cert__icontains=queryset) |
            Q(fecha__icontains=queryset) |
            Q(uvi__icontains=queryset),
        ).distinct().order_by('nro_cert',)
    return render(request, 'certificado_lista_obra.html', {
        'certificados': certificados,
        'obra': obra
    })

def create_certificado(request):
    if request.method == 'GET':
        return render(request, 'certificado_crear.html', {
            'form': CertificadoForm
        })
    else:
        form = CertificadoForm(request.POST)
        if form.is_valid():
            nuevo_cert = form.save(commit=False)
            nuevo_cert.cargaCert = request.user
            nuevo_cert.save()
            return redirect('certificados')
