from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from . models import Obras
from . forms import ObraFormAll, ObraFormActas


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

    