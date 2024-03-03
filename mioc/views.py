from django.shortcuts import render

# Create your views here.


def index(request):
    saludo = 'Portal de Pedidos'
    creador = 'Lucas L.'
    return render(request, 'index.html', {
        'titulo': saludo,
        'creador': creador,
    })
