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
    user = usuario(nombre=str(u).strip())
    conn = manejadorDeConexion()
    while True:
        user.sesion = str(conn.getAvailableConnection())
        if len(list(usuario.objects.filter(sesion=user.sesion))) == 0:
            user.save()
            break
    conn.openProgram()
    conn.connList.Refresh()

    return conn.openSession(connectionName=user.sesion, usuario=user.nombre, contrasenia=c)

def acceso(request):
    r = {}
    try:
        if request.method == 'POST':
            print request.POST
            try:
                if len(usuario.objects.get(nombre=str(request.POST['usuario'])).sesion)>0:
                    r['resultado'] = str('#/error')
                    request.session['currentError'] = str('El Usuario '+str(request.POST['usuario']).upper()+' ya esta en uso...')
                    return HttpResponse(
                        json.dumps(r),
                        content_type="application/json; charset=UTF-8"
                    )
            except:
                pass
            acc = integracion(str(request.POST['usuario']), str(request.POST['clave']))
            if acc:
                user = usuario.objects.get(nombre=str(request.POST['usuario']).strip())
                try:
                    if str(acc)[0].isupper():
                        print 'donde kiero'
                        r['resultado'] = str('#/error')
                        request.session['currentError'] = str(acc)
                        user.delete()
                        print 'borro...'
                except:
                    request.session['usuario'] = user.nombre
                    request.session['sesionActiva'] = user.sesion
                    r['resultado'] = str('#/home')
            else:
                r['resultado'] = str('#/error')
                request.session['currentError'] = str('El Sistema Comercial(Sico Cnel) no esta disponible por el momento...')
            print "Usuario... " + str(r)
            return HttpResponse(
                json.dumps(r),
                content_type="application/json; charset=UTF-8"
            )
    except:
        print 'Error...'
        return HttpResponse(
            json.dumps(r),
            content_type="application/json; charset=UTF-8"
        )


def error(request):
    return render_to_response('error.html',
        {
            'msjError': request.session['currentError'],
            'code': "#/",
            'tiempo': 4
        },
        context_instance=RequestContext(request))