# coding=utf-8
from django.contrib.humanize.tests import now
from ingresos.models import estadoDeSolicitud, materialDeActividad
from inventario.models import detalleMaterialContrato, medidor, sello

__author__ = 'Jhonsson'

from ControlSystem.pComm.conexion import manejadorDeConexion


class ingresarCambioDeMaterial():
    def __init__(self, conexion, contrato):
        self.conn = manejadorDeConexion()
        self.conn.setActiveSession(conexion)
        self.sesion = self.conn.activeSession
        self.contrato=contrato
        self.ERROR = {
            'estado': None,
            'mensaje': 'Error no se pudo completar la acción requerida......',
            'solicitud': None
        }

    def elegirPunto(self, estado, actividad):
        operaciones = {
            0: self.pasoUno,
            1: self.pasoDos,
            11: self.tercerPaso,
            7: self.pasoCuatro,
            8: self.pasoCinco,
            10: self.pasoSeis,
            45: self.pasoSiete,
            451: self.pasoOcho,
            450: self.pasoNueve,
            457: self.pasoDiez,
        }
        return operaciones[estado](actividad)

    def pasoUno(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 43) == 'RECEPCION DE SOLICITUDES Y TRAMITES (NUEVO)' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PTRBSOLS'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '10'):
                    self.solicitudesNuevo = i
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:
                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[up]')
                sesion.autECLPS.SendKeys('[tab]')
                sesion.autECLPS.SendKeys('[pf6]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys(str(actividad.tipoDeSolicitud_id), 11, 37)
                sesion.autECLPS.SendKeys(str(actividad.motivoDeSolicitud_id), 13, 37)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[eraseeof]', 15, 37)
                sesion.autECLPS.SendKeys(str(actividad.cliente.cuenta), 15, 37)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SetCursorPos(6, 28)
                if str(sesion.autECLPS.GetText(6, 28, 2)) == '  ':
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys(str(actividad.ubicacionDelMedidor_id))
                sesion.autECLPS.SendKeys('[down]')
                if str(sesion.autECLPS.GetText(7, 28, 2)) == '  ':
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble.usoGeneral_id))
                    sesion.autECLPS.SetCursorPos(7, 32)
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble_id))
                sesion.autECLPS.SendKeys('[down]')
                if str(sesion.autECLPS.GetText(8, 28, 2)) == '  ':
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys('1', 8, 28)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf3]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                opcionSico = False
                for i in range(9, 20):
                    if str(sesion.autECLPS.GetText(i, 7, 44)).strip() == 'CONSULTA DE TODAS LAS SOLICITUDES EFECTUADAS' \
                        or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PCONGENT'
                            and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '4'):
                        self.solicitudesTodas = i
                        opcionSico = True
                        break
                    else:
                        sesion.autECLPS.SendKeys('[down]')
                if opcionSico:
                    sesion.autECLPS.SendKeys('1')
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()

                    sesion.autECLPS.SendKeys('[pf8]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    sesion.autECLPS.SendKeys('4')
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    sesion.autECLPS.SendKeys('[up')
                    sesion.autECLPS.SendKeys('[tab]')
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys(str(actividad.cliente.cuenta), 12, 5)
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    for i in range(13, 21):
                        if str(sesion.autECLPS.GetText(i, 5, 7)).strip() == str(actividad.cliente.cuenta) \
                            and str(sesion.autECLPS.GetText(i, 36, 2)).strip() == str(actividad.tipoDeSolicitud_id) \
                            and str(sesion.autECLPS.GetText(i, 67, 10)).strip() == '%02d/%02d/%04d' % (
                                    now.day,
                                    now.month,
                                    now.year,
                                ) \
                            and str(sesion.autECLPS.GetText(i, 79, 2)) == ' 1':
                            actividad.numeroDeSolicitud = int(str(sesion.autECLPS.GetText(i, 14, 6)).strip())
                            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=1)
                            break
                        else:
                            sesion.autECLPS.SendKeys('[down]')
                    if actividad.numeroDeSolicitud>0:
                        actividad.save(force_update=True)
                        sesion.autECLPS.SendKeys('[pf12]')
                        sesion.autECLOIA.WaitForAppAvailable()
                        sesion.autECLOIA.WaitForInputReady()
                        sesion.autECLPS.SendKeys('[pf12]')
                        sesion.autECLOIA.WaitForAppAvailable()
                        sesion.autECLOIA.WaitForInputReady()
                        return {
                            'estado': actividad.estadoDeSolicitud_id,
                            'mensaje': 'Solicitud creada correctamente',
                            'solicitud': actividad.numeroDeSolicitud
                        }

                    else:
                        return self.ERROR
                else:
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    return self.ERROR
            else:
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                return self.ERROR
        else:
            return self.ERROR

    def pasoDos(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 16, 38) == 'IMPRESION DE FORMULARIOS DE INSPECCION' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PCLCUIMF'
                        and str(sesion.autECLPS.GetText(i, 62, 2)) == '20'):
                    self.formImpresion = i
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:

                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[up')
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

                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=11)
                actividad.save(force_update=True)

                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                return {
                    'estado': actividad.estadoDeSolicitud_id,
                    'mensaje': 'Solicitud enviada para impresion al servidor',
                    'solicitud': actividad.numeroDeSolicitud
                }
            else:
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                return self.ERROR
        else:
            return self.ERROR

    def tercerPaso(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 16, 38) == 'DIGITAR INSPECCION DE CLIENTE' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PDIINCL'
                        and str(sesion.autECLPS.GetText(i, 62, 2)) == '20'):
                    self.formImpresion = i
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:

                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[eraseeof]')
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                inspector = sello.objects.filter(utilizado=actividad)[0].detalleMaterialContrato.contrato.codigoInstalador
                sesion.autECLPS.SendKeys('[down]')
                sesion.autECLPS.SendKeys('[eraseeof]')
                sesion.autECLPS.SendKeys(str(inspector), 5, 30)
                sesion.autECLPS.SendKeys('[down]')
                med = list(medidor.objects.filter(actividad__id=actividad.id))[0]
                if int(str(sesion.autECLPS.GetText(6, 30, 5)).strip()) == 0:
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    if int(med.voltaje) == 120:
                        sesion.autECLPS.SendKeys('3', 6, 30)
                    else:
                        sesion.autECLPS.SendKeys('4', 6, 30)
                sesion.autECLPS.SendKeys('[down]')
                sesion.autECLPS.SendKeys(str(actividad.materialDeLaRed_id), 7, 30)
                sesion.autECLPS.SendKeys('S', 7, 70)
                sesion.autECLPS.SendKeys('[down]')
                sesion.autECLPS.SendKeys('[down]')
                sesion.autECLPS.SendKeys(str(actividad.estadoDeLaInstalacion_id), 9, 30)
                sesion.autECLPS.SendKeys('[down]')
                if int(str(sesion.autECLPS.GetText(10, 30, 2)).strip()) == 0:
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys(str(actividad.tipoDeConstruccion_id), 10, 30)
                sesion.autECLPS.SendKeys('[down]')
                if int(str(sesion.autECLPS.GetText(11, 30, 2)).strip()) == 0:
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys(str(actividad.ubicacionDelMedidor_id), 11, 30)
                sesion.autECLPS.SendKeys('[down]')
                if str(sesion.autECLPS.GetText(12, 30, 2)).strip() == '':
                    sesion.autECLPS.SendKeys(str(actividad.tipoDeAcometidaRed_id), 12, 30)
                sesion.autECLPS.SendKeys('[down]')
                if str(sesion.autECLPS.GetText(13, 30, 2)).strip() == '':
                    sesion.autECLPS.SendKeys(str(actividad.tipoDeAcometidaRed_id), 13, 30)
                sesion.autECLPS.SendKeys('[down]')
                if int(str(sesion.autECLPS.GetText(14, 30, 2)).strip()) == 0:
                    sesion.autECLPS.SendKeys('[eraseeof]')
                    sesion.autECLPS.SendKeys(str(actividad.calibreDeLaRed_id), 14, 30)
                sesion.autECLPS.SendKeys('[down]')
                if str(sesion.autECLPS.GetText(15, 30, 1)).strip() == '':
                    sesion.autECLPS.SendKeys(str(actividad.claseRed_id), 15, 30)
                sesion.autECLPS.SendKeys('[down]')
                if int(str(sesion.autECLPS.GetText(16, 30, 1)).strip()) == 0:
                    ts = str(actividad.tipoDeConstruccion_id)
                    sesion.autECLPS.SendKeys('[eraseeof]', 16, 30)
                    sesion.autECLPS.SendKeys(ts[0], 16, 30)
                    sesion.autECLPS.SendKeys('[eraseeof]', 16, 34)
                    sesion.autECLPS.SendKeys(ts[1], 16, 34)
                    sesion.autECLPS.SendKeys('[eraseeof]', 16, 38)
                    sesion.autECLPS.SendKeys(ts[2], 16, 38)
                sesion.autECLPS.SendKeys('[down]')
                if int(str(sesion.autECLPS.GetText(17, 30, 2)).strip()) == 0:
                    sesion.autECLPS.SendKeys('[eraseeof]', 17, 30)
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble.usoGeneral_id), 17, 30)
                    sesion.autECLPS.SendKeys('[eraseeof]', 17, 34)
                    sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble_id), 17, 34)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[eraseeof]', 6, 26)
                sesion.autECLPS.SendKeys('[eraseeof]', 6, 30)
                modelo = med.modelo_id
                sesion.autECLPS.SendKeys(str(modelo).split('-')[0], 6, 26)
                sesion.autECLPS.SendKeys(str(modelo).split('-')[1], 6, 30)
                sesion.autECLPS.SendKeys('[down]')
                sesion.autECLPS.SendKeys('[eraseeof]', 7, 26)
                if int(med.voltaje) == 120:
                    sesion.autECLPS.SendKeys('3', 7, 26)
                else:
                    sesion.autECLPS.SendKeys('4', 7, 26)
                sesion.autECLPS.SendKeys('[down]')
                sesion.autECLPS.SendKeys('[eraseeof]', 8, 26)
                sesion.autECLPS.SendKeys(str(actividad.demanda_id), 8, 26)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=7)
                actividad.save(force_update=True)

                return {
                    'estado': actividad.estadoDeSolicitud_id,
                    'mensaje': 'Solicitud enviada para impresion al servidor',
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                return self.ERROR
        else:
            return self.ERROR

    def pasoCuatro(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'CAMBIOS DE MEDIDOR' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '42'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 16, 21) == 'ASIGNAR MATERIAL TIPO' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PSESOLI'
                        and str(sesion.autECLPS.GetText(i, 62, 2)) == '40'):
                    self.formImpresion = i
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:

                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[up')
                sesion.autECLPS.SendKeys('[tab]')
                sesion.autECLPS.SendKeys('[eraseeof]')
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
                sesion.autECLPS.SendKeys('2')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                i = 8
                materiales = list(materialDeActividad.objects.filter(
                    actividad=actividad,
                    material__material__descargableDeSico=True,
                    material__proporcionado=True))
                for m in materiales:
                    sesion.autECLPS.SendKeys('[eraseeof]', i, 6)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[:2], i, 6)
                    for i in range(4):
                        sesion.autECLPS.SendKeys('[rigth]')
                    sesion.autECLPS.SendKeys('[eraseeof]', i, 10)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[2:4], i, 10)
                    for i in range(4):
                        sesion.autECLPS.SendKeys('[rigth]')
                    sesion.autECLPS.SendKeys('[eraseeof]', i, 14)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[4:6], i, 14)
                    for i in range(4):
                        sesion.autECLPS.SendKeys('[rigth]')
                    sesion.autECLPS.SendKeys('[eraseeof]', i, 18)
                    sesion.autECLPS.SendKeys(m.material.material.claveEnSico[6:9], i, 18)
                    if m.material.material.claveEnSico == '079058500':
                        sesion.autECLPS.SendKeys(',', 8, 73)
                    sesion.autECLPS.SendKeys('%02d' % m.cantidad, 8, 72)
                    sesion.autECLPS.SendKeys('[enter]')
                    i = sesion.autECLPS.GetCursorPosRow()

                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('9')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('A', 13, 43)
                sesion.autECLPS.SendKeys('[eraseeof]', 14, 43)
                sesion.autECLPS.SendKeys('%02d/%02d/%04d' % (now.day, now.month, now.year), 14, 43)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[pf5]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=8)
                actividad.save(force_update=True)

                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                return {
                    'estado': actividad.estadoDeSolicitud.id,
                    'mensaje': 'Materiales asignados a la solicitud',
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                return self.ERROR
        else:
            return self.ERROR

    def pasoAcceso(self):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 25) == 'INSTALACION - DESCONEXION' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '36'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '40'):
                self.cambiosDeMedidor = i
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('1')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            return True
        else:
            return False

    def pasoCinco(self, actividad):
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('1')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[pf6]')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]')
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud))
            sesion.autECLPS.SendKeys('1', 8, 32)
            sesion.autECLPS.SendKeys('2', 8, 35)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=10)
            actividad.save(force_update=True)

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            return {
                'estado': actividad.estadoDeSolicitud_id,
                'mensaje': 'Generada solicitud a bodega...',
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            return self.ERROR

    def pasoSeis(self, actividad):
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
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=45)
            actividad.save(force_update=True)

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            return {
                'estado': actividad.estadoDeSolicitud_id,
                'mensaje': actividad.estadoDeSolicitud.descripcion,
                'solicitud': actividad.numeroDeSolicitud
            }
        else:
            return self.ERROR

    def pasoSiete(self, actividad):
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

            sesion.autECLPS.SendKeys('1')    #451
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]')
            sesion.autECLPS.SendKeys('%02d%02d%04d' % (now.day, now.month, now.year))
            sesion.autECLPS.SendKeys(str(actividad.horaDeActividad)[:5], 7, 42)
            inspector = self.contrato.codigoInstalador
            sesion.autECLPS.SendKeys(str(inspector), 7, 42)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=451)
            actividad.save(force_update=True)

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            return {
                'estado': actividad.estadoDeSolicitud_id,
                'mensaje': actividad.estadoDeSolicitud.descripcion,
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            return self.ERROR

    def pasoOcho(self, actividad):
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
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=450)
            actividad.save(force_update=True)

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            return {
                'estado': actividad.estadoDeSolicitud_id,
                'mensaje': actividad.estadoDeSolicitud.descripcion,
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            return self.ERROR

    def pasoNueve(self, actividad):
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

            sesion.autECLPS.SendKeys('7')    #457
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sel=''
            baja=True
            for s in list(sello.objects.filter(utilizado=actividad)):
                sesion.autECLPS.SendKeys('[eraseeof]', 11, 26)
                sesion.autECLPS.SendKeys(s.numero, 11, 26)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                if str(s.numero).strip() != str(sesion.autECLPS.GetText(12, 26, 10)).strip():
                    sel=str(s.numero)
                    baja=False
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

                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=457)
                actividad.save(force_update=True)
                retorno = {
                    'estado': actividad.estadoDeSolicitud_id,
                    'mensaje': actividad.estadoDeSolicitud.descripcion,
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                retorno = {
                    'estado': None,
                    'mensaje': 'Sello %s no encontrado, posiblementa ya esta utilizado' % str(sel),
                    'solicitud': None
                }

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            sesion.autECLPS.SendKeys('[pf12]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            return retorno

        else:
            return self.ERROR

    def pasoDiez(self, actividad):
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

            sesion.autECLPS.SendKeys('9')    #459
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[pf9]')
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=13)
            actividad.save(force_update=True)

            titulo = sesion.autECLPS.GetText(9, 16, 20)
            while titulo != 'CONSULTA DE CLIENTES':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(9, 16, 20)

            return {
                'estado': actividad.estadoDeSolicitud_id,
                'mensaje': actividad.estadoDeSolicitud.descripcion,
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            return self.ERROR