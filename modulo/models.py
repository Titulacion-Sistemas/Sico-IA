# coding=utf-8
from django.db import models

# Create your models here.


class modulo(models.Model):
    nombre = models.CharField(max_length=10, verbose_name='Modulo', primary_key=True)
    descripcion = models.CharField(max_length=1, default='')

    def __unicode__(self):
        return '%s - %s' % (self.nombre, self.descripcion)