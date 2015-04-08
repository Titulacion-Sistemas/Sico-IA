# coding=utf-8
from django.db import models

# Create your models here.


class usuario(models.Model):
    nombre = models.CharField(max_length=10, verbose_name='Usuario de Sico', primary_key=True)
    sesion = models.CharField(max_length=1, verbose_name='Nombre de Sesion', default='')

    def __unicode__(self):
        return '%s - %s' % (self.nombre, self.sesion)

    class Meta:
        verbose_name = 'Usuario de Sico'
        verbose_name_plural = 'Usuarios de Sico'