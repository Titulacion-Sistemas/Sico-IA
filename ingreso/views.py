# coding=utf-8

import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from Sico_IA.pComm.conexion import manejadorDeConexion
from ingreso.models import usuario
from modulo.models import modulo


def index(request):
    try:
        if request.session['usuario']:
            return HttpResponseRedirect('/home/')
    except:
        pass
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def login(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

def espera(request):
    return render_to_response('espera.html', {}, context_instance=RequestContext(request))

def home(request):
    try:
        if request.session['usuario']:
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
            return render_to_response('home.html',
                {
                    'user': request.session['usuario'],
                    'sesion': request.session['sesionActiva'],
                    'modulos': json.dumps(var)
                }
            , context_instance=RequestContext(request))
    except:
        pass
    return HttpResponseRedirect('/salir/')

def integracion(u, c):
    user = usuario(nombre=str(u))
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
                if usuario.objects.get(nombre=str(request.POST['usuario']).strip().upper()).sesion:
                    r['resultado'] = str('#/error')
                    request.session['currentError'] = str('El Usuario '+str(request.POST['usuario']).upper()+' ya esta en uso...')
                    print 'Usuario actualmente en uso...'
                    return HttpResponse(
                        json.dumps(r),
                        content_type="application/json; charset=UTF-8"
                    )
            except:
                pass
            acc = integracion(str(request.POST['usuario']).strip().upper(), str(request.POST['clave']))
            if acc:
                user = usuario.objects.get(nombre=str(request.POST['usuario']).strip().upper())
                try:
                    if acc[0].isupper():
                        r['resultado'] = str('#/error')
                        request.session['currentError'] = str(acc)
                        user.sesion=''
                        user.save()
                except:
                    request.session['usuario'] = user.nombre.upper()
                    request.session['sesionActiva'] = user.sesion
                    r['resultado'] = str('/home/')
            else:
                try:
                    u = usuario.objects.get(nombre=str(request.POST['usuario']).strip())
                    if not u.sesion:
                        u.sesion=''
                except:
                    pass
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
    msjError = request.session['currentError']
    print msjError
    request.session['currentError'] = None
    return render_to_response('error.html',
        {
            'msjError': msjError,
            'code': "#/",
            'tiempo': 4
        },
        context_instance=RequestContext(request))

def cerrarSico(sesionAct):
    c = manejadorDeConexion()
    c.closeProgram(sesionAct)

def salir(request):
    try:
        user = usuario.objects.get(nombre=str(request.session['usuario']))
        cerrarSico(user.sesion)
        user.sesion = ''
        user.save()
    except:
        pass
    request.session['usuario'] = None
    request.session['sesionActiva'] = None
    return HttpResponseRedirect('/')


def principal(request):
    return render_to_response('principal.html', {}, context_instance=RequestContext(request))



