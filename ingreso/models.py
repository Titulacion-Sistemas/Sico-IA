# coding=utf-8
import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
from Sico_IA import settings


class usuario(models.Model):
    nombre = models.CharField(max_length=10, verbose_name='Usuario de Sico', primary_key=True)
    sesion = models.CharField(max_length=1, verbose_name='Nombre de Sesion', default='')

    def __unicode__(self):
        return '%s - %s' % (self.nombre, self.sesion)

    class Meta:
        verbose_name = 'Usuario de Sico'
        verbose_name_plural = 'Usuarios de Sico'

class turno(models.Model):
    t = models.SmallIntegerField(verbose_name='Turno')

    def __unicode__(self):
        return str(self.t)


class codigo (models.Model):
    dato =  models.CharField(max_length=15, verbose_name='Dato', primary_key=True)

    def __unicode__(self):
        return str(self.dato)

class ubicacion(models.Model):
    codigo = models.ForeignKey(codigo)
    latitud = models.DecimalField(max_digits=20, decimal_places=10)
    longitud = models.DecimalField(max_digits=20, decimal_places=10)
    latzone =  models.CharField(verbose_name='LatZone', max_length=20)
    longzone =  models.CharField(verbose_name='LongZone', max_length=20)
    aleste = models.DecimalField(max_digits=20, decimal_places=10)
    alnorte = models.DecimalField(max_digits=20, decimal_places=10)
    precision = models.DecimalField(max_digits=8, decimal_places=4)
    instante = models.CharField(max_length=50, default=str(timezone.localtime(timezone.now())))

    def __unicode__(self):
        return str(self.codigo.dato) + " - " + str(self.instante)