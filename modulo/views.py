import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ingreso.models import usuario
from ingreso.views import integracion
from modulo.models import modulo


def toplinks(request):
    r = {}
    if request.method == 'POST':
        print request.POST

        r = modulo.objects.filter(submodulo='')
        #for a in r:


    return HttpResponse(
        json.dumps(r),
        content_type="application/json; charset=UTF-8"
    )
