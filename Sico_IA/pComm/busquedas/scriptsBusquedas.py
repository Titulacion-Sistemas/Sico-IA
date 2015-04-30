# coding=utf-8

from django.shortcuts import render_to_response
import pythoncom
from Sico_IA.pComm.conexion import manejadorDeConexion


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
    cli = {}
    global lectura
    lectura = sesion.autECLPS.GetText(8, 35, 9).strip()
    cli['ci_ruc'] = sesion.autECLPS.GetText(4, 10, 13).strip()
    cli['cuenta'] = sesion.autECLPS.GetText(3, 27, 7).strip()
    cli['nombre'] = sesion.autECLPS.GetText(3, 35, 30).strip()
    #cli['direccion'] = sesion.autECLPS.GetText(14, 18, 50)
    #cli['interseccion'] = sesion.autECLPS.GetText(15, 18, 50)
    #cli['urbanizacion'] = sesion.autECLPS.GetText(16, 18, 50)
    cli['estado'] = sesion.autECLPS.GetText(21, 42, 20).strip()
    cli['geocodigo'] = str(
        '%02d.%02d.%02d.%03d.%07d' % (
            int(sesion.autECLPS.GetText(18, 13, 2)),
            int(sesion.autECLPS.GetText(18, 45, 2)),
            int(sesion.autECLPS.GetText(19, 13, 2)),
            int(sesion.autECLPS.GetText(20, 7, 3)),
            int(sesion.autECLPS.GetText(20, 73, 7)),
        )
    )

    cli['ubicacionGeografica'] = {
        'parroquia': (sesion.autECLPS.GetText(13, 17, 35)).encode('utf-8').strip(),
        'calle': (sesion.autECLPS.GetText(14, 18, 50)).encode('utf-8').strip(),
        'interseccion': (sesion.autECLPS.GetText(15, 18, 50)).encode('utf-8').strip(),
        'urbanizacion':(sesion.autECLPS.GetText(16, 18, 50)).encode('utf-8').strip()
    }
    #print cli.ubicacionGeografica

    sesion.autECLPS.SendKeys('[pf2]')
    sesion.autECLOIA.WaitForAppAvailable()
    sesion.autECLOIA.WaitForInputReady()

    cli['meses'] = sesion.autECLPS.GetText(12, 45, 3)
    cli['deuda'] = sesion.autECLPS.GetText(15, 22, 12)

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

        if actualmenteInstalado:
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
                    'marca': sesion.autECLPS.GetText(6, 29, 20).strip(),
                    'tecnologia': sesion.autECLPS.GetText(16, 29, 18).strip(),
                    'tension': (sesion.autECLPS.GetText(17, 29, 23)).encode('utf-8'),
                    'amperaje': sesion.autECLPS.GetText(18, 29, 17).strip(),
                    'fechaDeInstalacion': sesion.autECLPS.GetText(8, 29, 10),
                    'fechaDeDesinstalacion': sesion.autECLPS.GetText(9, 29, 10),
                    'lecturaDeInstalacion': sesion.autECLPS.GetText(8, 68, 9).strip(),
                    'lecturaDeDesinstalacion': sesion.autECLPS.GetText(9, 68, 9).strip(),
                    'fabrica': sesion.autECLPS.GetText(7, 29, 11).strip(),
                    'serie': miSerie,
                    'voltaje': miVoltaje,
                    'lectura': lect,
                    'tipo': sesion.autECLPS.GetText(5, 29, 16).strip(),
                    'digitos': sesion.autECLPS.GetText(11, 29, 2).strip(),
                    'fases': sesion.autECLPS.GetText(11, 68, 2).strip(),
                    'hilos': sesion.autECLPS.GetText(12, 29, 2).strip()
                }
            )
            sesion.autECLPS.SendKeys("[pf12]")
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            #sesion.autECLPS.Wait(900)
        sesion.autECLPS.SendKeys("[down]")
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        it += 1
        fab = sesion.autECLPS.GetText(it, 28, 1)

    return medidores


class buscar:
    def __init__(self, conexion):
        self.conn = manejadorDeConexion()
        self.conn.setActiveSession(conexion)
        self.sesion = self.conn.activeSession


    #busqueda por cuenta
    def porCuenta(self, cuenta):
        sesion = self.sesion
        sesion.autECLPS.SendKeys('5', 9, 12)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('1', 9, 3)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
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
                        'id': i - 9,
                        'cuenta': sesion.autECLPS.GetText(i, 5, 7),
                        'nombre': sesion.autECLPS.GetText(i, 13, 23),

                        'ubicacionGeografica': {
                            'parroquia': '',
                            'calle': (sesion.autECLPS.GetText(i, 37, 16)).encode('utf-8').strip(),
                            'interseccion': '',
                            'urbanizacion': ''
                        },

                        #direccion=sesion.autECLPS.GetText(i, 37, 16),
                        'deuda': sesion.autECLPS.GetText(i, 59, 8),
                        'meses': sesion.autECLPS.GetText(i, 68, 4)
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

        titulo = sesion.autECLPS.GetText(5, 1, 11)
        while titulo != '5=Programas':
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            titulo = sesion.autECLPS.GetText(5, 1, 11)

        #print titulo

        data = {
            'cClientes': coincidencias,
            'formCliente': formC,
            'cMedidores': medidores,
        }

        return data

    #busqueda por medidor
    def porMedidor(self, medidor):
        sesion = self.sesion
        sesion.autECLPS.SendKeys('5', 9, 12)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('1', 9, 3)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
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
                        'id': i - 9,

                        'ubicacionGeografica': {
                            'parroquia': '',
                            'calle': (sesion.autECLPS.GetText(i, 58, 20)).encode('utf-8').strip(),
                            'interseccion': '',
                            'urbanizacion': (sesion.autECLPS.GetText(i, 8, 11)).encode('utf-8').strip()
                        },

                        #urbanizacion=sesion.autECLPS.GetText(i, 8, 11),
                        #direccion=sesion.autECLPS.GetText(i, 58, 20),
                        'estado': sesion.autECLPS.GetText(i, 20, 3),
                        'cuenta': sesion.autECLPS.GetText(i, 24, 7),
                        'nombre': sesion.autECLPS.GetText(i, 32, 25),

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

        try:
            coincidencias.insert(0, llenarCliente(sesion))
        except:
            coincidencias.append(llenarCliente(sesion))

        sesion.autECLPS.SendKeys('1')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('9')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        medidores = llenarMedidores(sesion)

        titulo = sesion.autECLPS.GetText(5, 1, 11)
        while titulo != '5=Programas':
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            titulo = sesion.autECLPS.GetText(5, 1, 11)

        formC = coincidencias[0]

        data = {
            'cClientes': coincidencias,
            'formCliente': formC,
            'cMedidores': medidores,
        }

        return data


    #busqueda por nombre
    def porNombre(self, nombre):
        sesion = self.sesion
        sesion.autECLPS.SendKeys('5', 9, 12)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('1', 9, 3)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
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
                        'id': i - 9,
                        'nombre': sesion.autECLPS.GetText(i, 5, 22),

                        'ubicacionGeografica': {
                            'parroquia': '',
                            'calle': (sesion.autECLPS.GetText(i, 28, 17)).encode('utf-8').strip(),
                            'interseccion': '',
                            'urbanizacion': ''
                        },

                        #direccion=sesion.autECLPS.GetText(i, 28, 17),
                        'cuenta': sesion.autECLPS.GetText(i, 46, 7),
                        'deuda': sesion.autECLPS.GetText(i, 59, 8),
                        'meses': sesion.autECLPS.GetText(i, 68, 3)
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

        try:
            coincidencias[0] = llenarCliente(sesion)
        except:
            coincidencias.append(llenarCliente(sesion))

        sesion.autECLPS.SendKeys('9')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        medidores = llenarMedidores(sesion)

        titulo = sesion.autECLPS.GetText(5, 1, 11)
        while titulo != '5=Programas':
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            titulo = sesion.autECLPS.GetText(5, 1, 11)

        formC = coincidencias[0]

        data = {
            'cClientes': coincidencias,
            'formCliente': formC,
            'cMedidores': medidores,
        }

        return data


    #busqueda por ruta de lectura
    def porGeocodigo(self, geocodigo):
        sesion = self.sesion
        sesion.autECLPS.SendKeys('5', 9, 12)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('1', 12, 3)
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
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
                        'id': i - 9,

                        'ubicacionGeografica': {
                            'parroquia': '',
                            'calle': (sesion.autECLPS.GetText(i, 38, 14)).encode('utf-8').strip(),
                            'interseccion': ruta + '.' +(sesion.autECLPS.GetText(i, 5, 7)).encode('utf-8').strip(),
                            'urbanizacion': (sesion.autECLPS.GetText(i, 53, 10)).encode('utf-8').strip()
                        },

                        #interseccion=ruta+'.'+str(sesion.autECLPS.GetText(i, 5, 7)).strip(),
                        #direccion=sesion.autECLPS.GetText(i, 38, 14),
                        #urbanizacion=sesion.autECLPS.GetText(i, 53, 10),
                        'cuenta': sesion.autECLPS.GetText(i, 13, 7),
                        'nombre': sesion.autECLPS.GetText(i, 21, 16),
                        'deuda': sesion.autECLPS.GetText(i, 68, 8)
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

        try:
            coincidencias.insert(0, llenarCliente(sesion))
        except:
            coincidencias.append(llenarCliente(sesion))
        if coincidencias[0].geocodigo != geocodigo:
            return None

        sesion.autECLPS.SendKeys('9')
        sesion.autECLPS.SendKeys('[enter]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        medidores = llenarMedidores(sesion)

        titulo = sesion.autECLPS.GetText(5, 1, 11)
        while titulo != '5=Programas':
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            titulo = sesion.autECLPS.GetText(5, 1, 11)

        formC = coincidencias[0]

        data = {
            'cClientes': coincidencias,
            'formCliente': formC,
            'cMedidores': medidores,
        }

        return data


    def busquedaDeTipo(self, tipo, data):
        operaciones = {
            'porCuenta': self.porCuenta,
            'porMedidor': self.porMedidor,
            'porNombre': self.porNombre,
            'porGeocodigo': self.porGeocodigo
        }

        return operaciones[str(tipo)](data)


    def renderBusqueda(self, tipo, data):

        data = self.busquedaDeTipo(tipo, data)
        data['tipo'] = tipo


        return render_to_response('busquedas/'+tipo+'.html', data)