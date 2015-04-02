# coding=utf-8
from django.contrib.humanize.tests import now
import datetime
from ControlSystem.pComm.conexion import manejadorDeConexion
from ingresos.models import estadoDeSolicitud, materialDeActividad, detalleClienteMedidor, actividad
from inventario.models import sello, medidor

__author__ = 'Jhonsson'


class ingresarCambioDeMedidor():
    def __init__(self, conexion, contrato):
        self.conn = manejadorDeConexion()
        self.conn.setActiveSession(conexion)
        self.sesion = self.conn.activeSession
        self.contrato = contrato
        self.ERROR = {
            'estado': None,
            'mensaje': 'Error no se pudo completar la acción requerida......',
            'solicitud': None,
        }

    def elegirPunto(self, estado, act):
        operaciones = {
            0: self.pasoUno,
            1: self.pasoDos,
            6: self.tercerPaso,
            7: self.pasoCuatro,
            8: self.pasoCinco,
            10: self.pasoSeis,
            45: self.pasoSiete,
            451: self.pasoOcho,
            450: self.pasoNueve,
            457: self.pasoDiez,
            454: self.pasoOnce
        }
        act.horaDeActividad = str(act.horaDeActividad)[:8]
        return operaciones[estado](act)

    def pasoUno(self, actividad):
        sesion = self.sesion
        opcionSico = False
        print 'Paso 1'
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 51, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Cambio de medidor'

            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 43) == 'RECEPCION DE SOLICITUDES Y TRAMITES (NUEVO)' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PTRBSOLS'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '10'):
                    sesion.autECLPS.SendKeys('1', i, 3)
                    self.solicitudesNuevo = i
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Recepcion de solicitudes'

                sesion.autECLPS.SendKeys('[pf6]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Crear Solicitud'

                sesion.autECLPS.SendKeys('[eraseeof]', 11, 37)
                sesion.autECLPS.SendKeys(str(actividad.tipoDeSolicitud_id), 11, 37)
                sesion.autECLPS.SendKeys('[eraseeof]', 13, 37)
                sesion.autECLPS.SendKeys(str(actividad.motivoDeSolicitud_id), 13, 37)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[eraseeof]', 15, 37)
                sesion.autECLPS.SendKeys(str(actividad.cliente.cuenta), 15, 37)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                if str(sesion.autECLPS.GetText(2, 7, 7)).strip() == 'wALERTA':
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Cambio de medidor y/o acometida'

                ts = str(actividad.tipoDeServicio_id)
                sesion.autECLPS.SendKeys('[eraseeof]', 4, 25)
                sesion.autECLPS.SendKeys(str(ts[:1]), 4, 25)
                sesion.autECLPS.SendKeys('[eraseeof]', 4, 27)
                sesion.autECLPS.SendKeys(str(ts[1:2]), 4, 27)
                sesion.autECLPS.SendKeys('[eraseeof]', 4, 29)
                sesion.autECLPS.SendKeys(str(ts[2:3]), 4, 29)
                sesion.autECLPS.SendKeys('[left]')
                sesion.autECLPS.SendKeys('[eraseeof]', 6, 27)
                sesion.autECLPS.SendKeys(str(actividad.ubicacionDelMedidor_id), 6, 27)
                print str(actividad.ubicacionDelMedidor_id)+ ': bnd'
                if str(sesion.autECLPS.GetText(7, 27, 2)) == '  ':
                    sesion.autECLPS.SendKeys('[eraseeof]', 7, 27)
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble.usoGeneral_id), 7, 27)
                    sesion.autECLPS.SendKeys('[eraseeof]', 7, 30)
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble_id), 7, 30)
                if str(sesion.autECLPS.GetText(8, 30, 2)) == '  ':
                    sesion.autECLPS.SendKeys('[eraseeof]', 8, 30)
                    sesion.autECLPS.SendKeys('01', 8, 30)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                print 'Modelo de medidor'

                medidorInst = list(medidor.objects.filter(actividad=actividad, contrato__contrato=self.contrato))
                if medidorInst:
                    modelo = str(medidorInst[0].modelo_id).split('-')
                else:
                    modelo = ['NOR', '20']

                sesion.autECLPS.SendKeys('[eraseeof]', 10, 28)
                sesion.autECLPS.SendKeys(modelo[0], 10, 28)
                sesion.autECLPS.SendKeys('[eraseeof]', 10, 32)
                sesion.autECLPS.SendKeys(modelo[1], 10, 32)
                sesion.autECLPS.SendKeys('[eraseeof]', 12, 28)
                sesion.autECLPS.SendKeys(str(actividad.formaDeConexion_id), 12, 28)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                opcionSico = False
                for i in range(9, 20):
                    print str(sesion.autECLPS.GetText(i, 7, 45)).strip()
                    if str(sesion.autECLPS.GetText(i, 7, 45)).strip() == 'CONSULTA DE TODAS LAS SOLICITUDES EFECTUADAS' \
                        or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PCONGENT'
                            and str(sesion.autECLPS.GetText(i, 69, 2)).strip() == '4'):
                        self.solicitudesTodas = i
                        sesion.autECLPS.SendKeys('1', i, 3)
                        opcionSico = True
                        break
                if opcionSico:

                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    print 'Consulta de todas las solicitudes efectuadas '
                    sesion.autECLPS.SendKeys('[pf8]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    sesion.autECLPS.SendKeys('[eraseeof]', 7, 13)
                    sesion.autECLPS.SendKeys('4', 7, 13)
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    sesion.autECLPS.SendKeys('[up]')
                    sesion.autECLPS.SendKeys('[tab]')
                    sesion.autECLPS.SendKeys('[eraseeof]', 12, 5)
                    sesion.autECLPS.SendKeys(str(actividad.cliente.cuenta), 12, 5)
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    for i in range(13, 21):
                        if str(sesion.autECLPS.GetText(i, 5, 7)).strip() == str(actividad.cliente.cuenta) \
                            and str(sesion.autECLPS.GetText(i, 36, 2)).strip() == str(actividad.tipoDeSolicitud_id) \
                            and str(sesion.autECLPS.GetText(i, 67, 10)).strip() == '%d/%02d/%04d' % (
                                    int(datetime.datetime.today().day),
                                    int(datetime.datetime.today().month),
                                    int(datetime.datetime.today().year),
                                ) \
                            and str(sesion.autECLPS.GetText(i, 78, 2)) == '1 ':
                            actividad.numeroDeSolicitud = str(sesion.autECLPS.GetText(i, 14, 6)).strip()
                            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=1)
                            print 'Solicitud encontrada'
                            break
                        else:
                            sesion.autECLPS.SendKeys('[down]')

                    if int(actividad.numeroDeSolicitud) > 0:
                        actividad.save(force_update=True)
                        sesion.autECLPS.SendKeys('[pf12]')
                        sesion.autECLOIA.WaitForAppAvailable()
                        sesion.autECLOIA.WaitForInputReady()

                        sesion.autECLPS.SendKeys('[pf12]')
                        sesion.autECLOIA.WaitForAppAvailable()
                        sesion.autECLOIA.WaitForInputReady()
                        print 'Pantalla Principal - Estado = '+str(actividad.estadoDeSolicitud_id)
                        return {
                            'estado': str(actividad.estadoDeSolicitud_id),
                            'mensaje': 'Solicitud creada correctamente',
                            'solicitud': actividad.numeroDeSolicitud
                        }

                    else:
                        titulo = sesion.autECLPS.GetText(5, 1, 11)
                        while titulo != '5=Programas':
                            sesion.autECLPS.SendKeys('[pf12]')
                            sesion.autECLOIA.WaitForAppAvailable()
                            sesion.autECLOIA.WaitForInputReady()
                            titulo = sesion.autECLPS.GetText(5, 1, 11)
                        print 'Error 1'
                        return self.ERROR
                else:
                    titulo = sesion.autECLPS.GetText(5, 1, 11)
                    while titulo != '5=Programas':
                        sesion.autECLPS.SendKeys('[pf12]')
                        sesion.autECLOIA.WaitForAppAvailable()
                        sesion.autECLOIA.WaitForInputReady()
                        titulo = sesion.autECLPS.GetText(5, 1, 11)
                    print 'Error 2'
                    return self.ERROR
            else:
                titulo = sesion.autECLPS.GetText(5, 1, 11)
                while titulo != '5=Programas':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(5, 1, 11)
                print 'Error 3'
                return self.ERROR
        else:
            return self.ERROR

    def pasoDos(self, actividad):
        sesion = self.sesion
        opcionSico = False
        print 'Paso 2'
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 51, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Cambios de Medidor'
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                print str(sesion.autECLPS.GetText(i, 7, 38)).strip()
                if sesion.autECLPS.GetText(i, 7, 38) == 'IMPRESION DE FORMULARIOS DE INSPECCION' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PCLCUIMF'
                        and str(sesion.autECLPS.GetText(i, 69, 2)) == '20'):
                    self.formImpresion = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Impresion de formularios de inspeccion'
                sesion.autECLPS.SendKeys('[up]')
                sesion.autECLPS.SendKeys('[tab]')
                sesion.autECLPS.SendKeys('[eraseeof]')
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('6')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Cambio de estado'
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=6)
                actividad.save(force_update=True)
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Pantalla Principal'

                return {
                    'estado': str(actividad.estadoDeSolicitud_id),
                    'mensaje': 'Solicitud enviada para impresion al servidor',
                    'solicitud': actividad.numeroDeSolicitud
                }
            else:
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Error 1'
                return self.ERROR
        else:
            print 'Error 2'
            return self.ERROR

    def tercerPaso(self, actividad):
        sesion = self.sesion
        opcionSico = False
        print 'Paso 3'
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 51, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Cambios de medidor'
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                print str(sesion.autECLPS.GetText(i, 7, 38)).strip()
                if str(sesion.autECLPS.GetText(i, 7, 38)).strip() == 'DIGITAR INSPECCION DE CLIENTE' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PDIINCL'
                        and str(sesion.autECLPS.GetText(i, 69, 2)) == '20'):
                    self.formImpresion = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Digitar inspeccion de cliente'
                sesion.autECLPS.SendKeys('[up]')
                sesion.autECLPS.SendKeys('[tab]')
                sesion.autECLPS.SendKeys('[eraseeof]')
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Actualizar datos de inspeccion'

                sesion.autECLPS.SendKeys('[eraseeof]', 4, 30)
                sesion.autECLPS.SendKeys('%02d%02d%04d' % (
                    int(actividad.fechaDeActividad.day),
                    int(actividad.fechaDeActividad.month),
                    int(actividad.fechaDeActividad.year)
                ), 4, 30)

                inspector = self.contrato.codigoInstalador
                sesion.autECLPS.SendKeys('[eraseeof]', 5, 30)
                sesion.autECLPS.SendKeys(str(inspector), 5, 30)
                med = list(medidor.objects.filter(actividad__id=actividad.id, contrato__contrato=self.contrato))[0]
                if str(sesion.autECLPS.GetText(6, 30, 5)).strip() == '0':
                    sesion.autECLPS.SendKeys('[eraseeof]', 6, 30)
                    if int(med.voltaje) == 120:
                        sesion.autECLPS.SendKeys('3', 6, 30)
                    else:
                        sesion.autECLPS.SendKeys('4', 6, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 7, 30)
                sesion.autECLPS.SendKeys(str(actividad.materialDeLaRed_id), 7, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 7, 70)
                sesion.autECLPS.SendKeys('S', 7, 70)
                sesion.autECLPS.SendKeys('[eraseeof]', 9, 30)
                sesion.autECLPS.SendKeys(str(actividad.estadoDeLaInstalacion_id)[0], 9, 30)
                if str(sesion.autECLPS.GetText(10, 30, 2)).strip() == '0':
                    sesion.autECLPS.SendKeys('[eraseeof]', 10, 30)
                    sesion.autECLPS.SendKeys(str(actividad.tipoDeConstruccion_id), 10, 30)
                if str(sesion.autECLPS.GetText(11, 30, 2)).strip() == '' or str(sesion.autECLPS.GetText(11, 30, 2)).strip() == '0':
                    sesion.autECLPS.SendKeys('[eraseeof]', 11, 30)
                    sesion.autECLPS.SendKeys(str(actividad.ubicacionDelMedidor_id), 11, 30)
                if str(sesion.autECLPS.GetText(12, 30, 2)).strip() == '' or str(sesion.autECLPS.GetText(12, 30, 2)).strip() == '0':
                    sesion.autECLPS.SendKeys('[eraseeof]', 12, 30)
                    sesion.autECLPS.SendKeys(str(actividad.tipoDeAcometidaRed_id), 12, 30)
                if str(sesion.autECLPS.GetText(13, 30, 2)).strip() == '':
                    sesion.autECLPS.SendKeys('[eraseeof]', 13, 30)
                    sesion.autECLPS.SendKeys(str(actividad.tipoDeAcometidaRed_id), 13, 30)
                if str(sesion.autECLPS.GetText(14, 30, 2)).strip() == '0':
                    sesion.autECLPS.SendKeys('[eraseeof]', 14, 30)
                    sesion.autECLPS.SendKeys(str(actividad.calibreDeLaRed_id), 14, 30)
                if str(sesion.autECLPS.GetText(15, 30, 1)).strip() == '':
                    sesion.autECLPS.SendKeys('[eraseeof]', 15, 30)
                    sesion.autECLPS.SendKeys(str(actividad.claseRed_id), 15, 30)

                ts = str(actividad.tipoDeServicio_id)
                sesion.autECLPS.SendKeys('[eraseeof]', 16, 30)
                sesion.autECLPS.SendKeys(ts[0], 16, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 16, 34)
                sesion.autECLPS.SendKeys(ts[1], 16, 34)
                sesion.autECLPS.SendKeys('[eraseeof]', 16, 38)
                sesion.autECLPS.SendKeys(ts[2], 16, 38)

                if str(sesion.autECLPS.GetText(17, 30, 2)).strip() == '' or str(sesion.autECLPS.GetText(17, 30, 2)).strip() == '0':
                    sesion.autECLPS.SendKeys('[eraseeof]', 17, 30)
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble.usoGeneral_id), 17, 30)
                    sesion.autECLPS.SendKeys('[eraseeof]', 17, 34)
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble_id), 17, 34)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                print 'Medidor - Modelo'
                modelo = str(med.modelo_id).split('-')
                sesion.autECLPS.SendKeys('[eraseeof]', 6, 26)
                sesion.autECLPS.SendKeys(modelo[0], 6, 26)
                sesion.autECLPS.SendKeys('[eraseeof]', 6, 30)
                sesion.autECLPS.SendKeys(modelo[1], 6, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 7, 26)
                if int(med.voltaje) == 120:
                    sesion.autECLPS.SendKeys('3', 7, 26)
                else:
                    sesion.autECLPS.SendKeys('4', 7, 26)
                sesion.autECLPS.SendKeys('[pf4]', 8, 26)
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=7)
                actividad.save(force_update=True)

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                print 'Cambio de estado a 7'

                titulo = sesion.autECLPS.GetText(5, 1, 11)
                while titulo != '5=Programas':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(5, 1, 11)

                return {
                    'estado': str(actividad.estadoDeSolicitud_id),
                    'mensaje': 'Solicitud enviada para impresion al servidor',
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                titulo = sesion.autECLPS.GetText(5, 1, 11)
                while titulo != '5=Programas':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(5, 1, 11)
                print 'Error 1'
                return self.ERROR
        else:
            titulo = sesion.autECLPS.GetText(5, 1, 11)
            while titulo != '5=Programas':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(5, 1, 11)
            print 'Error 2'
            return self.ERROR

    def pasoCuatro(self, actividad):
        sesion = self.sesion
        opcionSico = False
        print 'Paso 4'
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 51, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                opcionSico = True
                sesion.autECLPS.SendKeys('5', i, 12)
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Cambios de Medidor'
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                print str(sesion.autECLPS.GetText(i, 7, 21)).strip()
                if str(sesion.autECLPS.GetText(i, 7, 21)).strip() == 'ASIGNAR MATERIAL TIPO' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PSESOLI'
                        and str(sesion.autECLPS.GetText(i, 69, 2)) == '40'):
                    self.formImpresion = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Asignar material tipo'
                sesion.autECLPS.SendKeys('[up]')
                sesion.autECLPS.SendKeys('[tab]')
                sesion.autECLPS.SendKeys('[eraseeof]')
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('2')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Descargar material'
                i = 8
                materiales = list(materialDeActividad.objects.filter(
                    actividad=actividad,
                    material__material__descargableDeSico=True,
                    material__proporcionado=True))
                for m in materiales:
                    sesion.autECLPS.SendKeys('[eraseeof]', i, 6)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[:2], i, 6)

                    sesion.autECLPS.SendKeys('[eraseeof]', i, 10)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[2:4], i, 10)

                    sesion.autECLPS.SendKeys('[eraseeof]', i, 14)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[4:6], i, 14)

                    sesion.autECLPS.SendKeys('[eraseeof]', i, 18)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[6:9], i, 18)

                    sesion.autECLPS.SendKeys('[eraseeof]', i, 67)
                    #sesion.autECLPS.SendKeys('0', i, 72)
                    if m.material.material.claveEnSico == '079058500':
                        sesion.autECLPS.SendKeys('0,'+'%02d' % m.cantidad, i, 72)
                    else:
                        sesion.autECLPS.SendKeys('0.'+'%02d' % m.cantidad, i, 72)
                    #sesion.autECLPS.SendKeys('%02d' % m.cantidad, i, 74)

                    if i == 17:
                        i = 8
                    else:
                        i = 1+i
                    print u'Descargado '+unicode(m)

                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Material descargado'
                sesion.autECLPS.SendKeys('9')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Aprobacion de solicitud materiales'
                sesion.autECLPS.SendKeys('A', 13, 43)
                sesion.autECLPS.SendKeys('[eraseeof]', 14, 43)
                sesion.autECLPS.SendKeys('%02d%02d%04d' % (
                                    int(datetime.datetime.today().day),
                                    int(datetime.datetime.today().month),
                                    int(datetime.datetime.today().year),
                                ), 14, 43
                )
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                print 'Cambio de estado'
                sesion.autECLPS.SendKeys('[pf5]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=8)
                actividad.save(force_update=True)

                print 'Pantalla principal'
                titulo = sesion.autECLPS.GetText(5, 1, 11)
                while titulo != '5=Programas':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(5, 1, 11)

                return {
                    'estado': actividad.estadoDeSolicitud.id,
                    'mensaje': 'Materiales asignados a la solicitud',
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                titulo = sesion.autECLPS.GetText(5, 1, 11)
                while titulo != '5=Programas':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(5, 1, 11)
                print 'Error 1'
                return self.ERROR
        else:
            print 'Error 2'
            return self.ERROR

    def pasoAcceso(self):
        sesion = self.sesion
        opcionSico = False
        print 'Para acceso'
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if str(sesion.autECLPS.GetText(i, 16, 25)).strip() == 'INSTALACION - DESCONEXION' \
                or (str(sesion.autECLPS.GetText(i, 51, 3)).strip() == '36'
                    and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '40'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Instalacion desconexion'
            sesion.autECLPS.SendKeys('1')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Completo I - D'
            return True
        else:
            print 'Error I - D'
            return False

    def pasoCinco(self, actividad):
        print 'Paso 5'
        if self.pasoAcceso():
            sesion = self.sesion

            sesion.autECLPS.SendKeys('1')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[pf6]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Crear solicitud materiales a bodega'

            sesion.autECLPS.SendKeys('[eraseeof]', 6, 34)
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud), 6, 34)
            sesion.autECLPS.SendKeys('[eraseeof]', 8, 31)
            sesion.autECLPS.SendKeys('1', 8, 31)
            sesion.autECLPS.SendKeys('[eraseeof]', 8, 34)
            sesion.autECLPS.SendKeys('2', 8, 34)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Cambia Estado de Solicitud 10'
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=10)
            actividad.save(force_update=True)

            print 'Regresar a pantalla principal'
            titulo = sesion.autECLPS.GetText(5, 1, 11)
            while titulo != '5=Programas':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(5, 1, 11)

            return {
                'estado': str(actividad.estadoDeSolicitud_id),
                'mensaje': 'Generada solicitud a bodega...',
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            print 'Error 1'
            return self.ERROR

    def pasoSeis(self, actividad):
        print 'Paso 6'
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('2')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[eraseeof]', 8, 6)
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud), 8, 6)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('1')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Cambio de estado a 45'
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=45)
            actividad.save(force_update=True)

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            #sesion.autECLPS.SendKeys('[pf12]')
            #sesion.autECLOIA.WaitForAppAvailable()
            #sesion.autECLOIA.WaitForInputReady()
            print 'Pantalla Principal'
            return {
                'estado': str(actividad.estadoDeSolicitud_id),
                'mensaje': actividad.estadoDeSolicitud.descripcion.encode('utf-8'),
                'solicitud': actividad.numeroDeSolicitud
            }
        else:
            print 'Error 1'
            return self.ERROR

    def pasoSiete(self, actividad):
        print 'Paso 7'
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]', 9, 7)
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print '451'
            sesion.autECLPS.SendKeys('1')    #451
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Fecha de Actividad'
            sesion.autECLPS.SendKeys('[eraseeof]', 6, 42)
            sesion.autECLPS.SendKeys(
                '%02d%02d%04d' % (
                    int(actividad.fechaDeActividad.day),
                    int(actividad.fechaDeActividad.month),
                    int(actividad.fechaDeActividad.year),
                ), 6, 42
            )
            sesion.autECLPS.SendKeys('[eraseeof]', 7, 42)
            sesion.autECLPS.SendKeys(str(actividad.horaDeActividad)[:5], 7, 42)
            inspector = self.contrato.codigoInstalador
            sesion.autECLPS.SendKeys('[eraseeof]', 8, 42)
            sesion.autECLPS.SendKeys(str(inspector), 8, 42)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Cambio de estado 451'
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=451)
            actividad.save(force_update=True)

            titulo = sesion.autECLPS.GetText(5, 1, 11)
            while titulo != '5=Programas':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(5, 1, 11)
            print 'Pantalla Principal'
            return {
                'estado': str(actividad.estadoDeSolicitud_id),
                'mensaje': actividad.estadoDeSolicitud.descripcion.encode('utf-8'),
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            print 'Error 1'
            return self.ERROR

    def pasoOcho(self, actividad):
        print 'Paso 8'
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]')
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print '450'
            sesion.autECLPS.SendKeys('0')    #450
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            pag = False
            i = 0
            while i < 5:
                if i == 4 and str(sesion.autECLPS.GetText(((i * 2) + 9), 76, 1)) == '+':
                    pag = True
                cm = str(sesion.autECLPS.GetText(((i * 2) + 8), 72, 2))
                if cm == ' 0':
                    cm = str(sesion.autECLPS.GetText(((i * 2) + 8), 75, 2))
                    cm = ',%s' % cm
                elif cm == '  ':
                    break
                else:
                    cm = '.%s' % cm
                sesion.autECLPS.SendKeys(cm, ((i * 2) + 9), 74)
                if pag:
                    i = 0
                    sesion.autECLPS.SendKeys('[roll up]')
                    pag = False
                else:
                    i += 1

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Datos Modificados'
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=450)
            actividad.save(force_update=True)
            print 'Estado cambiado a 450'
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Pantalla principal'
            return {
                'estado': str(actividad.estadoDeSolicitud_id),
                'mensaje': actividad.estadoDeSolicitud.descripcion.encode('utf-8'),
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            print 'Error 1'
            return self.ERROR

    def pasoNueve(self, actividad):
        print 'Paso 9'
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]')
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print '457'
            sesion.autECLPS.SendKeys('7')    #457
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sel = ''
            baja = True
            for s in list(sello.objects.filter(utilizado=actividad)):
                sesion.autECLPS.SendKeys('[eraseeof]', 11, 26)
                sesion.autECLPS.SendKeys(s.numero, 11, 26)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                if str(s.numero).strip() != str(sesion.autECLPS.GetText(12, 26, 10)).strip():
                    sel = str(s.numero)
                    baja = False
                    break

            if baja:
                for s in list(sello.objects.filter(utilizado=actividad)):
                    sesion.autECLPS.SendKeys('[eraseeof]', 11, 26)
                    sesion.autECLPS.SendKeys(s.numero, 11, 26)
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    sesion.autECLPS.SendKeys('4')
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                print 'Estado cambiado a 457'
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=457)
                actividad.save(force_update=True)
                retorno = {
                    'estado': str(actividad.estadoDeSolicitud_id),
                    'mensaje': actividad.estadoDeSolicitud.descripcion.encode('utf-8'),
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                print 'Error de sello utilizado...'
                retorno = {
                    'estado': None,
                    'mensaje': 'Sello %s no encontrado, posiblementa ya esta utilizado' % str(sel),
                    'solicitud': None
                }

            titulo = sesion.autECLPS.GetText(5, 1, 11)
            while titulo != '5=Programas':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(5, 1, 11)
            print 'Pagina principal'

            return retorno

        else:
            return self.ERROR

    def pasoDiez(self, actividad):
        print 'Paso 10'
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]')
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print '454'
            sesion.autECLPS.SendKeys('4')    #454
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print 'Medidores instalados al cliente'
            i = 10
            f = str(sesion.autECLPS.GetText(i, 56, 10))
            returno = self.ERROR
            while f.strip() != '0/00/0000' or f.strip() != '00/00/0000' or i==20:
                i += 1

            if i < 20:
                sesion.autECLPS.SendKeys('4', i, 4)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('s')
                med = list(medidor.objects
                .filter(actividad__id=actividad.id)
                .exclude(contrato__contrato=self.contrato)
                )[0]
                sesion.autECLPS.SendKeys('[eraseeof]', 11, 70)
                sesion.autECLPS.SendKeys(str(med.lectura), 11, 70)
                sesion.autECLPS.SendKeys('[pf2]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                med=list(medidor.objects
                .filter(actividad__id=actividad.id, contrato__contrato=self.contrato)
                )[0]
                sesion.autECLPS.SendKeys(str(med.tipo)[:1], 6, 9)
                sesion.autECLPS.SendKeys(str(med.marca.id)[:3], 6, 13)
                sesion.autECLPS.SendKeys(str(med.fabrica), 6, 18)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                if str(med.fabrica).strip() == str(sesion.autECLPS.GetText(7, 18, 11)).strip():
                    sesion.autECLPS.SendKeys('1', 7, 6)
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    print 'Medidor Asignado'

                    sesion.autECLPS.SendKeys('s')
                    sesion.autECLPS.SendKeys('[eraseeof]', 10, 62)
                    sesion.autECLPS.SendKeys(med.lectura, 10, 62)
                    sesion.autECLPS.SendKeys('[pf2]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()

                    actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=454)
                    actividad.save(force_update=True)

                    returno={
                        'estado': str(actividad.estadoDeSolicitud_id),
                        'mensaje': actividad.estadoDeSolicitud.descripcion.encode('utf-8'),
                        'solicitud': actividad.numeroDeSolicitud
                    }
                else:
                    print 'Medidor no asignado'
                    titulo = sesion.autECLPS.GetText(5, 1, 11)
                    while titulo != '5=Programas':
                        sesion.autECLPS.SendKeys('[pf12]')
                        sesion.autECLOIA.WaitForAppAvailable()
                        sesion.autECLOIA.WaitForInputReady()
                        titulo = sesion.autECLPS.GetText(5, 1, 11)
                    return returno
            else:
                print 'No hay medidores para desconectar'
                titulo = sesion.autECLPS.GetText(5, 1, 11)
                while titulo != '5=Programas':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(5, 1, 11)
                return returno
            print 'Error desconocido'
            titulo = sesion.autECLPS.GetText(5, 1, 11)
            while titulo != '5=Programas':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(5, 1, 11)

            return returno

        else:
            print 'Error 1'
            return self.ERROR

    def pasoOnce(self, actividad):
        print 'Paso 11'
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]')
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            print '459 confirmar datos de instalacion'
            sesion.autECLPS.SendKeys('9')    #459
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[pf9]')
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=13)
            actividad.save(force_update=True)
            print 'Cambia estado a 13'
            titulo = sesion.autECLPS.GetText(5, 1, 11)
            while titulo != '5=Programas':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(5, 1, 11)

            print 'Completo, se procede a realizar cambios locales'

            medidorDes = list(medidor.objects.filter(actividad=actividad).exclude(contrato__contrato=self.contrato))[0]
            enlace = detalleClienteMedidor.objects.get(
                medidor = medidorDes,
                cliente = actividad.cliente
            )
            enlace.lectura_desinstalacion=medidorDes.lectura
            enlace.fecha_desinstalacion=datetime.datetime.today()
            enlace.save(force_update=True)
            print 'Detalle cliente medidor modificado'
            medidorInst = medidor.objects.filter(actividad=actividad, contrato__contrato=self.contrato).first()
            enlace = detalleClienteMedidor(
                lectura_instalacion = medidorInst.lectura,
                fecha_instalacion = now.date(),
                medidor = medidorInst,
                cliente = actividad.cliente
            )
            enlace.save()
            print 'Detalle cliente medidor realizado'

            return {
                'estado': str(actividad.estadoDeSolicitud_id),
                'mensaje': actividad.estadoDeSolicitud.descripcion.encode('utf-8'),
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            return self.ERROR