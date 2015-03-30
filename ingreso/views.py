from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext


def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def login(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))