# coding=utf-8
from decimal import Decimal
import json
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import time
from Sico_IA.pComm.busquedas.scriptsBusquedas import buscar
from ingreso.models import usuario, turno, codigo, ubicacion
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

    return render_to_response('busquedas/busquedas.html', data, context_instance=RequestContext(request))


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
            datos = str(dict(form.errors)['__all__'])

        return HttpResponse(
                json.dumps(datos),
                content_type="application/json; charset=UTF-8"
            )
    else:
        return None


def busquedaAndroid(request, tipo, dato):
    if request.method == 'GET':

        jsn = JSONMiddleware()
        jsn.process_request(request)

        print request.GET


        dato = str(dato).replace("_", " ")
        dato = dato.strip()

        t = turno(t=turno.objects.all().count())
        t.save()

        contador = 0

        while turno.objects.all().first() != t and contador < 50:
            time.sleep(1)
            contador += 1

        if contador >= 50:
            t.delete()
            return None

        b = buscar('A')
        print str(dato)
        print str(tipo)
        datos = b.busquedaDeTipo(str(tipo), str(dato))

        t.delete()

        return HttpResponse(
                json.dumps(datos),
                content_type="application/json; charset=UTF-8"
            )
    else:
        return None


def cambiosdemedidor(request):
    return render_to_response('combiosdemedidor/cambiodemedidor.html', {}, context_instance=RequestContext(request))





def geoAndroid(request, dato, lat, long, precision,  latzone, longzone, aleste, alnorte):
    from django.utils import timezone
    if request.method == 'GET':

        jsn = JSONMiddleware()
        jsn.process_request(request)

        print request.GET


        dato = str(dato).replace("_", " ")
        dato = dato.strip()

        if len(codigo.objects.all().filter(dato=str(dato)))>0:

            code = codigo.objects.get(dato=str(dato))
            print "se actualizó " + str(code)
        else:

            code = codigo(dato=str(dato))
            code.save()
            print "se guardó " + str(code)

        g = ubicacion(
            codigo=code,
            latitud=Decimal(str(lat)),
            longitud=Decimal(str(long)),
            latzone=latzone,
            longzone=longzone,
            aleste=Decimal(str(aleste)),
            alnorte=Decimal(str(alnorte)),
            precision=Decimal(str(precision))
        )

        g.save()

        return HttpResponse(
            json.dumps(True),
            content_type="application/json; charset=UTF-8"
        )

    else:
        return None
