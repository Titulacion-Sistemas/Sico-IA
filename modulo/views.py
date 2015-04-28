import json
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from Sico_IA.pComm.busquedas.scriptsBusquedas import buscar
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


def busquedacriterio(request):
    if request.method == 'POST':
        form = busquedas(request.POST['formulario'])

        if form.is_valid():

            b = buscar(request.session['sesionActiva'])
            datos = b.busquedaDeTipo(form.data['criterio'], form.data['dato'])

            return {
                'coincidencias':{
                    'titulo': 'Coincidencias',
                    'contenido': datos['cClientes']
                },
                'cliente':{
                    'titulo': 'Datos de Cliente',
                    'contenido': datos['formCliente']
                },
                'medidores':{
                    'titulo': 'Medidores del Cliente',
                    'contenido': datos['cMedidores']
                }
            }
        else:
            return {
                'coincidencias':{
                    'titulo': 'Error',
                    'contenido': form.errors
                }
            }
    else:
        return render_to_response('busquedas/criterio.html', {}, context_instance=RequestContext(request))

