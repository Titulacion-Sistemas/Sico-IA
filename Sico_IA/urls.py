# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ingreso.views.index', name='index'),

    url(r'^login/$', 'ingreso.views.login', name='login'),
    url(r'^espera/$', 'ingreso.views.espera', name='espera'),
    url(r'^acceso/$', 'ingreso.views.acceso', name='acceso'),
    url(r'^error/$', 'ingreso.views.error', name='error'),
    url(r'^home/$', 'ingreso.views.home', name='home'),
    url(r'^salir/$', 'ingreso.views.salir', name='salir'),
    url(r'^principal/$', 'ingreso.views.principal', name='principal'),

    url(r'^enconstruccion/$', 'modulo.views.enconstruccion', name='enconstruccion'),

    url(r'^busquedas/$', 'modulo.views.busquedas', name='busquedas'),

    url(r'^busquedacriterio/$', 'modulo.views.busquedacriterio', name='busquedacriterio'),

    url(r'^cambiosdemedidor/$', 'modulo.views.cambiosdemedidor', name='cambiosdemedidor'),

    url(r'^bandroid/([^/]+)/([^/]+)/$', 'modulo.views.busquedaAndroid', name='bandroid'),

     url(r'^geoandroid/([^/]+)/([^/]+)/([^/]+)/([^/]+)/([^/]+)/([^/]+)/([^/]+)/([^/]+)/$',
         'modulo.views.geoAndroid', name='geoandroid'),

)