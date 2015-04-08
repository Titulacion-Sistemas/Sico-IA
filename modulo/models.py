# coding=utf-8
from django.db import models
from ingreso.models import *

# Create your models here.


class modulo(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    valor = models.CharField(max_length=50, verbose_name='Modulo', null=True, blank=True, default='')
    descripcion = models.CharField(max_length=100, null=True, blank=True, default='')
    submodulo = models.ForeignKey('modulo', verbose_name='Es submodulo de', null=True, blank=True)
    tipo = models.IntegerField(max_length=3, verbose_name='Tipo de Solicitud', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.valor


class estado(models.Model):
    numero=models.PositiveSmallIntegerField(verbose_name='codigo', editable=True)
    descripcion=models.CharField(max_length=60)
    modulo = models.ManyToManyField(modulo)

    def __unicode__(self):
        return u'%s : %s' % (str(self.numero), self.descripcion)

    class Meta:
        verbose_name_plural="Estados de Solicitud"
        verbose_name='Estado de Solicitud'


class dato(models.Model):
    VOLT = (
        ('CUENTA', 'CUENTA'),
        ('MEDIDOR', 'MEDIDOR'),
        ('NOMBRE', 'NOMBRE'),
        ('GEOCÓDIGO', 'GEOCÓDIGO'),
        ('SOLICITUD', 'SOLICITUD'),
    )
    tipo = models.CharField(max_length=20, choices=VOLT, default='CUENTA')
    valor = models.CharField(max_length=18, primary_key=True)
    modulo = models.ForeignKey(modulo)

    def __unicode__(self):
        return u'%s: %s' % (self.tipo, self.valor)


class vitacora(models.Model):
    usuario = models.ForeignKey(usuario)
    dato = models.ForeignKey(dato)
    estado = models.ForeignKey(estado, null=True, blank=True, default='')
    tiempo = models.DateTimeField(verbose_name='Fecha y Hora', auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s' % (self.dato, str(self.tiempo))


