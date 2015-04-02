# coding=utf-8

import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from Sico_IA.pComm.conexion import manejadorDeConexion
from ingreso.models import usuario


def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def login(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

def espera(request):
    return render_to_response('espera.html', {}, context_instance=RequestContext(request))

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def integracion(u, c):
    conn = None
    user = usuario(nombre=str(u).strip())
    while True:
        conn = manejadorDeConexion()
        user.sesion = str(conn.getAvailableConnection())
        if not usuario.objects.filter(sesion=user.sesion):
            user.save()
            break
    return conn.openSession(connectionName=user.sesion, usuario=user.nombre, contrasenia=c)

def acceso(request):
    if request.method == 'POST':
        print request.POST

        r = {}
        if integracion(str(request.POST['usuario']), str(request.POST['clave'])):
            user = usuario.objects.get(nombre=str(request.POST['usuario']).strip())
            request.session['usuario'] = user
            r['resultado'] = '#/home'
            print 'a home'
        else:
            r['resultado'] = '#/error'
            request.session['currentError'] = 'El Sistema Comercial(Sico Cnel) no esta disponible por el momento...'
            print 'error'


        print "Usuario... " + str(request.POST['usuario'])
        return HttpResponse(json.dumps(r), content_type="application/json")


def error(request):
    return render_to_response('error.html',
        {
            'msjError': request.session['currentError'],
            'code': "window.setTimeout('window.location.assign("+str("\"/\"")+")',3000);"
        },
        context_instance=RequestContext(request))