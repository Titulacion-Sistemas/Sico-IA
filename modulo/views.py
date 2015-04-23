import json
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from ingreso.models import usuario
from ingreso.views import integracion
from modulo.models import modulo
from modulo.forms import busquedas as busq


def enconstruccion(request):
    return render_to_response('enconstruccion.html', {}, context_instance=RequestContext(request))


def busquedas(request):
    form = busq()
    submodulos=[]
    for sub in modulo.objects.filter(submodulo=modulo.objects.get(nombre='busquedas')):
        submodulos.append({
            'nombre': sub.valor,
            'link': sub.nombre
        })
    data = {
        'form': form,
        'submodulos': json.dumps(submodulos)
    }

    return render_to_response('busquedas.html', data, context_instance=RequestContext(request))



def busquedaporcuenta(request):
    return render_to_response('busquedas/porcuenta.html', {}, context_instance=RequestContext(request))


def busquedapormedidor(request):
    return render_to_response('busquedas/pormedidor.html', {}, context_instance=RequestContext(request))


def busquedapornombre(request):
    return render_to_response('busquedas/pornombre.html', {}, context_instance=RequestContext(request))


def busquedaporgeocodigo(request):
    return render_to_response('busquedas/porgeocodigo.html', {}, context_instance=RequestContext(request))