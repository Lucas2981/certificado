from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from . models import Obras,EmpresaPoliza
from . forms import ObraFormAll, ObraFormActas,EmpresaPolizaForm
from django.contrib.auth.decorators import login_required, user_passes_test







# Create your views here.


def index(request):
    saludo = 'Portal de Pedidos'
    creador = 'Lucas L.'
    return render(request, 'index.html', {
        'titulo': saludo,
        'creador': creador,
    })

def obras(request):
    obras = Obras.objects.all()
    queryset = request.GET.get('buscar')
    if queryset:
        obras = Obras.objects.filter(
            Q(expedientes__icontains=queryset) |
            Q(institucion__name__icontains=queryset)|
            Q(inspector__fullname__icontains=queryset)|
            Q(empresa__name__icontains=queryset),
            ).distinct().order_by('institucion',)
    return render(request, 'obras.html',{'obras': obras, })

def obra_detalle(request,pk):
    if request.method == 'GET':
        pedido = get_object_or_404(Obras, pk=pk)
        form = ObraFormAll(instance=pedido)
        form2 = ObraFormActas(instance=pedido)
        return render(request, 'obra_detalle.html', {
            'form': form,
            'form2':form2,
            })
    else:
        try:
            pedido = get_object_or_404(Obras, pk=pk)
            form2 = ObraFormActas(request.POST, instance=pedido)
            form2.save()
            return redirect('obras')
        except ValueError:
            pedido = get_object_or_404(Obras, pk=pk)
            form = ObraFormAll(instance=pedido)
            return render(request, 'obra_detalle.html', {
            'form': form,
            'error': 'Error al validar pedido.'
            })

@login_required
def create_empresa(request):
    if request.method == 'GET':
        return render(request, 'fondo_reparo_crear.html', {
            'form': EmpresaPolizaForm
        })
    else:
        form = EmpresaPolizaForm(request.POST)
        if form.is_valid():
            nueva_empresa = form.save(commit=False)
            print(nueva_empresa.creaEmpresa)
            nueva_empresa.creaEmpresa = request.user
            print(nueva_empresa.creaEmpresa)
            nueva_empresa.save()
            return redirect('aseguradora')
        

def lista_empresa(request):
    empresa = EmpresaPoliza.objects.all()
    queryset = request.GET.get('buscar')
    if queryset:
        empresa = empresa.objects.filter(
            Q(empresa__icontains=queryset) |
            Q(location__icontains=queryset)|
            Q(telefono__icontains=queryset),
            ).distinct().order_by('empresa',)
    return render(request, 'empresa_lista.html',{'empresa': empresa, })