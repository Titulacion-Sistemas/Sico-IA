import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ingreso.models import usuario
from ingreso.views import integracion
from modulo.models import modulo


def toplinks(request):
    retorno={}
    if request.method == 'POST':
        print request.POST
        var=[]
        for r in modulo.objects.filter(submodulo=''):
            submodulos = []
            for sub in modulo.objects.filter(submodulo=r):
                submodulos.append({
                    'nombre': sub.valor,
                    'link': sub.nombre
                })
            var.append({
                'nombre': r.valor,
                'link': r.nombre,
                'submodulos': submodulos
            })
        print var

        retorno['modulos'] = var

    return HttpResponse(
        json.dumps(retorno),
        content_type="application/json; charset=UTF-8"
    )
