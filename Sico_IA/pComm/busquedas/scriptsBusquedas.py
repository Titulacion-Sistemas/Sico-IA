# coding=utf-8

from django.shortcuts import render_to_response
import pythoncom
import time
from Sico_IA.pComm.conexion import manejadorDeConexion
from ingreso.models import turno


lectura = '0'


def newVoltaje(ser):
    voltaje = 120

    try:
        if int(ser[:2])%2==0:
            print 'si'
            return 240
    except:
        try:
            if int(ser[1:3])%2==0:
                print 'si'
                return 240
        except:
            pass
    return voltaje


def llenarCliente(sesion):

    global lectura
    lectura = sesion.autECLPS.GetText(8, 35, 9).strip()
    cli = {
        '0': {'Ruc/Ci': sesion.autECLPS.GetText(4, 10, 13).strip()},
        '1': {'Cuenta': sesion.autECLPS.GetText(3, 27, 7).strip()},
        '2': {'Nombre': sesion.autECLPS.GetText(3, 35, 30).strip()},
        '3': {'Estado': sesion.autECLPS.GetText(21, 42, 20).strip()},
        '4': {'Geocodigo': str(
            '%02d.%02d.%02d.%03d.%07d' % (
                int(sesion.autECLPS.GetText(18, 13, 2)),
                int(sesion.autECLPS.GetText(18, 45, 2)),
                int(sesion.autECLPS.GetText(19, 13, 2)),
                int(sesion.autECLPS.GetText(20, 7, 3)),
                int(sesion.autECLPS.GetText(20, 73, 7)),
            )
        )},
        '5': {'Parroquia': (sesion.autECLPS.GetText(13, 17, 35)).encode('utf-8').strip()},
        '6': {'Direccion': (sesion.autECLPS.GetText(14, 18, 50)).encode('utf-8').strip()},
        '7': {'Interseccion': (sesion.autECLPS.GetText(15, 18, 50)).encode('utf-8').strip()},
        '8': {'Urbanizacion':(sesion.autECLPS.GetText(16, 18, 50)).encode('utf-8').strip()}
    }

    sesion.autECLPS.SendKeys('[pf2]')
    sesion.autECLOIA.WaitForAppAvailable()
    sesion.autECLOIA.WaitForInputReady()

    cli['9'] = {'Meses': sesion.autECLPS.GetText(12, 45, 3).strip()}
    cli['10'] = {'Deuda': sesion.autECLPS.GetText(15, 22, 12).strip()}

    sesion.autECLPS.SendKeys('[pf12]')
    sesion.autECLOIA.WaitForAppAvailable()
    sesion.autECLOIA.WaitForInputReady()

    for j in range(3):
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

    sesion.autECLPS.SendKeys('[pf12]')
    sesion.autECLOIA.WaitForAppAvailable()
    sesion.autECLOIA.WaitForInputReady()

    return cli


def llenarMedidores(sesion):
    medidores = []
    it = 9
    fab = sesion.autECLPS.GetText(it, 28, 1)
    while fab != " ":
        actualmenteInstalado = sesion.autECLPS.GetText(it, 59, 10) == ' 0/00/0000'

        if actualmenteInstalado:
            lect = lectura
        else:
            lect = '-'

        sesion.autECLPS.SendKeys("1")
        sesion.autECLPS.SendKeys("[enter]")
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys("[down]")
        miSerie = sesion.autECLPS.GetText(10, 29, 11).strip()
        miVoltaje = newVoltaje(miSerie)
        if not miSerie:
            miSerie='-'
        medidores.append(
            {
                '0': {'Fabrica': sesion.autECLPS.GetText(7, 29, 11).strip()},
                '1': {'Serie': miSerie},
                '2': {'Voltaje': miVoltaje},
                '3': {'Marca': sesion.autECLPS.GetText(6, 29, 20).strip()},
                '4': {'Lectura': lect},
                '5': {'Tecnologia': sesion.autECLPS.GetText(16, 29, 18).strip()},
                '6': {'Tension': (sesion.autECLPS.GetText(17, 29, 23)).encode('utf-8')},
                '7': {'Amperaje': sesion.autECLPS.GetText(18, 29, 17).strip()},
                '8': {'Fecha In.': sesion.autECLPS.GetText(8, 29, 10)},
                '9': {'Fecha Des.': sesion.autECLPS.GetText(9, 29, 10)},
                '10': {'Lect. In.': sesion.autECLPS.GetText(8, 68, 9).strip()},
                '11': {'Lect. Des.': sesion.autECLPS.GetText(9, 68, 9).strip()},
                '12': {'Tipo': sesion.autECLPS.GetText(5, 29, 16).strip()},
                '13': {'Digitos': sesion.autECLPS.GetText(11, 29, 2).strip()},
                '14': {'Fases': sesion.autECLPS.GetText(11, 68, 2).strip()},
                '15': {'Hilos': sesion.autECLPS.GetText(12, 29, 2).strip()}
            }
        )
        sesion.autECLPS.SendKeys("[pf12]")
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        #sesion.autECLPS.Wait(900)
        sesion.autECLPS.SendKeys("[down]")
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        it = it + 1
        fab = sesion.autECLPS.GetText(it, 28, 1)

    return medidores





class buscar:
    def __init__(self, conexion):
        self.conn = manejadorDeConexion()
        self.conn.setActiveSession(conexion)
        self.sesion = self.conn.activeSession

    def buscarEnMenu(self, stri, filIni, colIni, filplus, colPlus=79):
        sesion = self.sesion
        i=filIni
        data = str(sesion.autECLPS.GetText(filIni, colIni, len(stri)).strip())
        while data != stri:

            if i == filplus:
                if str(sesion.autECLPS.GetText(filplus, colPlus, 1).strip()) == '+':
                    sesion.autECLPS.SendKeys('[roll up]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    i = filIni
                    data = str(sesion.autECLPS.GetText(i, colIni, len(stri)).strip())
                else:
                    return None
            else:
                i += 1
                data = str(sesion.autECLPS.GetText(i, colIni, len(stri)).strip())

        return i

    def regresarInicio(self):
        sesion = self.sesion
        titulo = sesion.autECLPS.GetText(5, 1, 11)
        i=0
        while titulo != '5=Programas':
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            titulo = sesion.autECLPS.GetText(5, 1, 11)
            i+=1
            if i==100:
                return False
        return True

    #busqueda por cuenta
    def porCuenta(self, cuenta):
        sesion = self.sesion
        
        #fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        if fil:
            sesion.autECLPS.SendKeys('5', fil, 12)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        fil = self.buscarEnMenu('CONSULTA GENERAL DE CLIENTES', 9, 7, 22)
        if fil:
            sesion.autECLPS.SendKeys('1', fil, 3)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        sesion.autECLPS.SendKeys('[eraseeof]', 9, 5)
        sesion.autECLPS.SendKeys(str(cuenta), 9, 5)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        coincidencias = []
        for i in range(10, 21):
            if sesion.autECLPS.GetText(i, 5, 7).strip() != "":
                coincidencias.append(
                    {
                        
                        '0': {'Cuenta': sesion.autECLPS.GetText(i, 5, 7)},
                        '1': {'Nombre': sesion.autECLPS.GetText(i, 13, 23)},
                        '2': {'Direccion': (sesion.autECLPS.GetText(i, 37, 16)).encode('utf-8').strip()},
                        '3': {'Meses': sesion.autECLPS.GetText(i, 68, 4)},
                        '4': {'Deuda': sesion.autECLPS.GetText(i, 59, 8)}

                    }
                )

        sesion.autECLPS.SendKeys('1', 10, 3)
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        formC = llenarCliente(sesion)

        #if coincidencias[0].cuenta != cuenta:
        #    return None

        sesion.autECLPS.SendKeys('9')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        medidores = llenarMedidores(sesion)

        if self.regresarInicio():

            return {
                'coincidencias':{
                    'titulo': 'Coincidencias',
                    'contenido': coincidencias,
                    'show': True
                },
                'cliente':{
                    'titulo': 'Datos de Cliente',
                    'contenido': formC,
                    'show': True
                },
                'medidores':{
                    'titulo': 'Medidores del Cliente',
                    'contenido': medidores,
                    'show': True
                }
            }

        else:
            return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'

    #busqueda por medidor
    def porMedidor(self, medidor):
        sesion = self.sesion
        
        #fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        if fil:
            sesion.autECLPS.SendKeys('5', fil, 12)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        fil = self.buscarEnMenu('CONSULTA GENERAL DE CLIENTES', 9, 7, 22)
        if fil:
            sesion.autECLPS.SendKeys('1', fil, 3)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        sesion.autECLPS.SendKeys('[pf9]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        for h in range(3):
            sesion.autECLPS.SendKeys("[up]")
        sesion.autECLPS.SendKeys('[tab]')
        sesion.autECLPS.SendKeys(str(medidor), 4, 43)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        coincidencias = []
        for i in range(7, 18):
            if sesion.autECLPS.GetText(i, 8, 11).strip() != "":
                coincidencias.append(
                    {
                        '0': {'Medidor': (sesion.autECLPS.GetText(i, 8, 11)).encode('utf-8').strip()},
                        '1': {'Estado': sesion.autECLPS.GetText(i, 20, 3)},
                        '2': {'Cuenta': sesion.autECLPS.GetText(i, 24, 7)},
                        '3': {'Nombre': sesion.autECLPS.GetText(i, 32, 25)},
                        '4': {'Direccion': (sesion.autECLPS.GetText(i, 58, 20)).encode('utf-8').strip()}
                    }
                )

        sesion.autECLPS.SendKeys('2', 7, 4)
        #print 'se pulsoel 2'
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        formC = llenarCliente(sesion)

        sesion.autECLPS.SendKeys('1')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('9')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        medidores = llenarMedidores(sesion)

        if self.regresarInicio():

            return {
                'coincidencias':{
                    'titulo': 'Coincidencias',
                    'contenido': coincidencias,
                    'show': True
                },
                'cliente':{
                    'titulo': 'Datos de Cliente',
                    'contenido': formC,
                    'show': True
                },
                'medidores':{
                    'titulo': 'Medidores del Cliente',
                    'contenido': medidores,
                    'show': True
                }
            }

        else:
            return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'


    #busqueda por nombre
    def porNombre(self, nombre):
        sesion = self.sesion
        
        #fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        if fil:
            sesion.autECLPS.SendKeys('5', fil, 12)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        fil = self.buscarEnMenu('CONSULTA GENERAL DE CLIENTES', 9, 7, 22)
        if fil:
            sesion.autECLPS.SendKeys('1', fil, 3)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        sesion.autECLPS.SendKeys('[pf8]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys(str(nombre)[:17], 8, 5)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        coincidencias = []
        for i in range(9, 21):
            if sesion.autECLPS.GetText(i, 5, 22).strip() != "":
                coincidencias.append(
                    {
                        
                        '0': {'Nombre': sesion.autECLPS.GetText(i, 5, 22)},
                        '1': {'Cuenta': sesion.autECLPS.GetText(i, 46, 7)},
                        '2': {'Direccion': (sesion.autECLPS.GetText(i, 28, 17)).encode('utf-8').strip()},
                        '3': {'Meses': sesion.autECLPS.GetText(i, 68, 3)},
                        '4': {'Deuda': sesion.autECLPS.GetText(i, 59, 8)}

                    }
                )

        sesion.autECLPS.SendKeys('1', 9, 3)
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        formC = llenarCliente(sesion)

        sesion.autECLPS.SendKeys('9')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        medidores = llenarMedidores(sesion)

        if self.regresarInicio():

            return {
                'coincidencias':{
                    'titulo': 'Coincidencias',
                    'contenido': coincidencias,
                    'show': True
                },
                'cliente':{
                    'titulo': 'Datos de Cliente',
                    'contenido': formC,
                    'show': True
                },
                'medidores':{
                    'titulo': 'Medidores del Cliente',
                    'contenido': medidores,
                    'show': True
                }
            }

        else:
            return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'


    #busqueda por ruta de lectura
    def porGeocodigo(self, geocodigo):
        sesion = self.sesion
        
        #fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        fil = self.buscarEnMenu('CONSULTA DE CLIENTES', 9, 16, 22)
        if fil:
            sesion.autECLPS.SendKeys('5', fil, 12)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        fil = self.buscarEnMenu('CONSULTA DE CLIENTES POR SECTOR Y RUTA DE LECTURA', 9, 7, 22)
        if fil:
            sesion.autECLPS.SendKeys('1', fil, 3)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        else:
            if self.regresarInicio():
                return 'Error, el usuario de Sistema Comercial no esta habilitado para la opción deseada...'
            else:
                return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'
        sesion.autECLPS.SendKeys('[pf8]', 9, 5)
        geocodigo = geocodigo.split(".")
        sesion.autECLPS.SendKeys('[up]')
        sesion.autECLPS.SendKeys('[tab]')
        sesion.autECLPS.SendKeys(str('%02d' % (int(geocodigo[0]))), 8, 6)
        sesion.autECLPS.SendKeys('[tab]')
        sesion.autECLPS.SendKeys(str('%02d' % (int(geocodigo[1]))), 8, 11)
        sesion.autECLPS.SendKeys('[tab]')
        sesion.autECLPS.SendKeys(str('%02d' % (int(geocodigo[2]))), 8, 18)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('7', 9, 3)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[up]')
        sesion.autECLPS.SendKeys('[tab]')
        sesion.autECLPS.SendKeys('[eraseeof]')
        sesion.autECLPS.SendKeys(str('%03d' % (int(geocodigo[3]))), 8, 6)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('8', 9, 2)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[up]')
        sesion.autECLPS.SendKeys('[tab]')
        sesion.autECLPS.SendKeys('[eraseeof]', 8, 5)
        sesion.autECLPS.SendKeys(str('%07d' % (int(geocodigo[4]))), 8, 5)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        ruta = str(sesion.autECLPS.GetText(4, 16, 13)).strip()
        coincidencias = []
        for i in range(9, 21):
            if sesion.autECLPS.GetText(i, 5, 7).strip() != "":
                coincidencias.append(
                    {
                        '0': {'Geocodigo': ruta + '.' +(sesion.autECLPS.GetText(i, 5, 7)).encode('utf-8').strip()},
                        '1': {'Urbanizacion': (sesion.autECLPS.GetText(i, 53, 10)).encode('utf-8').strip()},
                        '2': {'Cuenta': sesion.autECLPS.GetText(i, 13, 7)},
                        '3': {'Nombre': sesion.autECLPS.GetText(i, 21, 16)},
                        '4': {'Direccion': (sesion.autECLPS.GetText(i, 38, 14)).encode('utf-8').strip()},
                        '5': {'Deuda': sesion.autECLPS.GetText(i, 68, 8)}
                    }
                )

        sesion.autECLPS.SendKeys('1', 9, 3)
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        formC = llenarCliente(sesion)

        #if coincidencias[0].geocodigo != geocodigo:
        #    return None

        sesion.autECLPS.SendKeys('9')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        medidores = llenarMedidores(sesion)

        if self.regresarInicio():

            return {
                'coincidencias':{
                    'titulo': 'Coincidencias',
                    'contenido': coincidencias,
                    'show': True
                },
                'cliente':{
                    'titulo': 'Datos de Cliente',
                    'contenido': formC,
                    'show': True
                },
                'medidores':{
                    'titulo': 'Medidores del Cliente',
                    'contenido': medidores,
                    'show': True
                }
            }

        else:
            return 'Error, se ha perdido la conexion, cierre sesion e intente nuevamente...'


    def busquedaDeTipo(self, tipo, data):

        t = turno(t=turno.objects.all().count())
        t.save()

        contador = 0

        while turno.objects.all().first() != t and contador < 50:
            time.sleep(1)
            contador += 1

        if contador >= 50:
            t.delete()
            return "Error busqueda en espera"

        operaciones = {
            'porCuenta': self.porCuenta,
            'porMedidor': self.porMedidor,
            'porNombre': self.porNombre,
            'porGeocodigo': self.porGeocodigo
        }
        result = operaciones[str(tipo)](data)
        t.delete()
        return result


    def renderBusqueda(self, tipo, data):

        data = self.busquedaDeTipo(tipo, data)
        data['tipo'] = tipo


        return render_to_response('busquedas/'+tipo+'.html', data)
