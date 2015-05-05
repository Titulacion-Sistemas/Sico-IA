import json
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from Sico_IA.pComm.busquedas.scriptsBusquedas import buscar
from ingreso.models import usuario
from ingreso.views import integracion
from modulo.models import modulo
from modulo.forms import busquedas as busq
from modulo.renderRequest import JSONMiddleware


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


def busquedacriterio(request):
    if request.method == 'POST':

        jsn = JSONMiddleware()
        jsn.process_request(request)
        print request.POST

        form = busq(data=QueryDict(request.POST['formulario']))

        if form.is_valid():

            b = buscar(request.session['sesionActiva'])
            datos = b.busquedaDeTipo(str(form.data['criterio']), str(form.data['dato']))

        else:
            datos = {
                'coincidencias':{
                    'titulo': 'Error',
                    'contenido': form.errors
                }
            }

        return HttpResponse(
                json.dumps(datos),
                content_type="application/json; charset=UTF-8"
            )
    else:
        return render_to_response('busquedas/coincidencias.html', {}, context_instance=RequestContext(request))







