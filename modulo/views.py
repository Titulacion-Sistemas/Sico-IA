import json
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from ingreso.models import usuario
from ingreso.views import integracion
from modulo.models import modulo


def enconstruccion(request):
    return render_to_response('enconstruccion.html', {}, context_instance=RequestContext(request))
