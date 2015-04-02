# coding=utf-8

import decimal
from ControlSystem.pComm.conexion import manejadorDeConexion


def llenarCliente(sesion):

    cli = []
    cli.append(sesion.autECLPS.GetText(4, 10, 13))
    cli.append(sesion.autECLPS.GetText(3, 27, 7))
    cli.append(sesion.autECLPS.GetText(3, 35, 30))
    cli.append(sesion.autECLPS.GetText(14, 18, 50))
    cli.append(sesion.autECLPS.GetText(15, 18, 50))
    cli.append(sesion.autECLPS.GetText(16, 18, 50))
    cli.append(sesion.autECLPS.GetText(21, 42, 20))
    cli.append(
        str(
            '%02d.%02d.%02d.%03d.%07d' % (
                int(sesion.autECLPS.GetText(18, 13, 2)),
                int(sesion.autECLPS.GetText(18, 45, 2)),
                int(sesion.autECLPS.GetText(19, 13, 2)),
                int(sesion.autECLPS.GetText(20, 7, 3)),
                int(sesion.autECLPS.GetText(20, 73, 7)),
            )
        )
    )
    cli.append(str(sesion.autECLPS.GetText(13, 13, 2).strip()))
    cli.append(str(sesion.autECLPS.GetText(13, 17, 35).strip()))
    #print(cli.geocodigo)
    sesion.autECLPS.SendKeys('[pf2]')
    sesion.autECLOIA.WaitForAppAvailable()
    sesion.autECLOIA.WaitForInputReady()

    cli.append(sesion.autECLPS.GetText(12, 45, 3))
    cli.append(str(decimal.Decimal(sesion.autECLPS.GetText(15, 22, 12))))

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
        sesion.autECLPS.SendKeys("1")
        sesion.autECLPS.SendKeys("[enter]")
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys("[down]")

        medidores.append(sesion.autECLPS.GetText(6, 29, 20))
        medidores.append(sesion.autECLPS.GetText(16, 29, 18))
        medidores.append((sesion.autECLPS.GetText(17, 29, 23)).encode('utf-8'))
        medidores.append(sesion.autECLPS.GetText(18, 29, 17))
        medidores.append(sesion.autECLPS.GetText(8, 29, 10))
        medidores.append(sesion.autECLPS.GetText(9, 29, 10))
        medidores.append(sesion.autECLPS.GetText(8, 68, 9))
        medidores.append(sesion.autECLPS.GetText(9, 68, 9))
        medidores.append(sesion.autECLPS.GetText(7, 29, 11))
        medidores.append(sesion.autECLPS.GetText(10, 29, 11))
        medidores.append(sesion.autECLPS.GetText(5, 29, 16))
        medidores.append(sesion.autECLPS.GetText(11, 29, 2))
        medidores.append(sesion.autECLPS.GetText(11, 68, 2))
        medidores.append(sesion.autECLPS.GetText(12, 29, 2))

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
                coincidencias.append(sesion.autECLPS.GetText(i, 5, 7))
                coincidencias.append(sesion.autECLPS.GetText(i, 13, 23))
                coincidencias.append(sesion.autECLPS.GetText(i, 37, 16))
                coincidencias.append(sesion.autECLPS.GetText(i, 59, 8))
                coincidencias.append(sesion.autECLPS.GetText(i, 68, 4))

        sesion.autECLPS.SendKeys('1', 10, 3)
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        cliente = llenarCliente(sesion)

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

        return [
            coincidencias,
            cliente,
            medidores
        ]

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
                coincidencias.append(sesion.autECLPS.GetText(i, 8, 11))
                coincidencias.append(sesion.autECLPS.GetText(i, 20, 3))
                coincidencias.append(sesion.autECLPS.GetText(i, 24, 7))
                coincidencias.append(sesion.autECLPS.GetText(i, 32, 25))
                coincidencias.append(sesion.autECLPS.GetText(i, 58, 20))

        sesion.autECLPS.SendKeys('2', 7, 4)
        #print 'se pulsoel 2'
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        cliente = llenarCliente(sesion)

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

        return [
            coincidencias,
            cliente,
            medidores
        ]


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
                coincidencias.append(sesion.autECLPS.GetText(i, 5, 22))
                coincidencias.append(sesion.autECLPS.GetText(i, 28, 17))
                coincidencias.append(sesion.autECLPS.GetText(i, 46, 7))
                coincidencias.append(sesion.autECLPS.GetText(i, 59, 8))
                coincidencias.append(sesion.autECLPS.GetText(i, 68, 3))

        sesion.autECLPS.SendKeys('1', 9, 3)
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        cliente = llenarCliente(sesion)

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

        return [
            coincidencias,
            cliente,
            medidores
        ]


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
        geocodigo=geocodigo.split(".")
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
                coincidencias.append(ruta+'.'+str(sesion.autECLPS.GetText(i, 5, 7)).strip())
                coincidencias.append(sesion.autECLPS.GetText(i, 13, 7))
                coincidencias.append(sesion.autECLPS.GetText(i, 21, 16))
                coincidencias.append(sesion.autECLPS.GetText(i, 38, 14))
                coincidencias.append(sesion.autECLPS.GetText(i, 53, 10))
                coincidencias.append(sesion.autECLPS.GetText(i, 68, 8))

        sesion.autECLPS.SendKeys('1', 9, 3)
        for j in range(4):
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
        sesion.autECLPS.SendKeys('[pf2]')
        sesion.autECLOIA.WaitForAppAvailable()
        sesion.autECLOIA.WaitForInputReady()

        cliente = llenarCliente(sesion)

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

        return [
            coincidencias,
            cliente,
            medidores
        ]

    def busquedaIntegrada(self, tipo, data):
        operaciones = {
            '1': self.porCuenta,
            '2': self.porMedidor,
            '3': self.porNombre,
            '4': self.porGeocodigo
        }
        return operaciones[str(tipo)](data)
