# coding=utf-8
from django.contrib.humanize.tests import now
from ControlSystem.pComm.conexion import manejadorDeConexion
from ingresos.models import *
from inventario.models import *

__author__ = 'Jhonsson'


class ingresarServicioNuevo():
    def __init__(self, conexion, contrato):
        self.conn = manejadorDeConexion()
        self.conn.setActiveSession(conexion)
        self.sesion = self.conn.activeSession
        self.contrato = contrato
        self.ERROR = {
            'estado': None,
            'mensaje': 'Error no se pudo completar la acción requerida......',
            'solicitud': None
        }

    def elegirPunto(self, estado, actividad):
        operaciones = {
            0: self.pasoUno,
            1: self.pasoDos,
            6: self.pasoTres,
            7: self.pasoCuatro,
            75: self.pasoCinco,
            8: self.pasoSeis,
            85: self.pasoSiete,
            9: self.pasoOcho,
            10: self.pasoNueve,
            45: self.pasoDiez,
            451: self.pasoOnce,
            450: self.pasoDoce,
            457: self.pasoCatorce,
            454: self.pasoQuince
        }
        return operaciones[estado](actividad)

    def pasoUno(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 18) == 'ATENCION DE SOLICITUDES' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '30'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '5'):
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
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 43) == 'RECEPCION DE SOLICITUDES Y TRAMITES (NUEVO)' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PTRBSOLS'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '5'):
                    self.solicitudesNuevo = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    sesion.autECLPS.SendKeys('[down]')
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf6]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[eraseeof]', 11, 37)
                sesion.autECLPS.SendKeys(str(actividad.tipoDeSolicitud_id), 11, 37)
                sesion.autECLPS.SendKeys('[eraseeof]', 13, 37)
                sesion.autECLPS.SendKeys(str(actividad.motivoDeSolicitud_id), 13, 37)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys(str(actividad.cliente.tipo), 8, 45)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys(str(actividad.cliente.ci_ruc), 7, 39)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                if str(sesion.autECLPS.GetText(9, 7, 25)).strip()=='':
                    nomb = str(actividad.cliente.nombre).split(' ')
                    c=int(len(nomb)/2)
                    sesion.autECLPS.SendKeys(str(' '.join(nomb[:c])), 9, 7)
                    sesion.autECLPS.SendKeys(str(' '.join(nomb[c:])), 10, 7)
                if str(sesion.autECLPS.GetText(12, 7, 9)).strip()=='':
                    sesion.autECLPS.SendKeys('1',12,7)
                if str(sesion.autECLPS.GetText(12, 64, 9)).strip()=='':
                    sesion.autECLPS.SendKeys('1',12,64)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                ref=list(detalleClienteReferencia.objects.filter(cliente=actividad.cliente))[0].referencia
                prov = '%02d' % ref.geocodigo.ruta.sector.canton.provincia.id
                cant = '%02d' % ref.geocodigo.ruta.sector.canton.num
                parr = '%02d' % ref.ubicacionGeografica.parroquia.num
                sesion.autECLPS.SendKeys(prov,6,28)
                sesion.autECLPS.SendKeys(cant,7,28)
                sesion.autECLPS.SendKeys(parr,8,28)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('C',4,58)
                sesion.autECLPS.SendKeys('CA',10,28)
                sesion.autECLPS.SendKeys('[pf4]',11,28)
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys(ref.ubicacionGeografica.calle.descripcion1,5,36)
                sesion.autECLPS.SendKeys('1',6,4)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                #posiblemente borrar todos los ceros a la izquierda
                sesion.autECLPS.SendKeys(str(ref.geocodigo)[6:16]+'.'+str(ref.geocodigo)[16:], 9, 27)
                med = medidor.objects.get(actividad=actividad, contrato__contrato=self.contrato)
                sesion.autECLPS.SendKeys('1', 14, 32)
                if med.voltaje==120:
                    sesion.autECLPS.SendKeys('2', 14, 35)
                else:
                    sesion.autECLPS.SendKeys('3', 14, 35)
                sesion.autECLPS.SendKeys('B', 14, 38)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                modeloMed = str(med.modelo.id).split('-')
                sesion.autECLPS.SendKeys(modeloMed[0],5,30)
                sesion.autECLPS.SendKeys('[eraseeof]', 5, 34)
                sesion.autECLPS.SendKeys(modeloMed[1],5,34)
                sesion.autECLPS.SendKeys('[eraseeof]', 7, 30)
                sesion.autECLPS.SendKeys(actividad.formaDeConexion_id, 7, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 9, 30)
                sesion.autECLPS.SendKeys('1', 9, 30)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                actividad.numeroDeSolicitud=int(str(sesion.autECLPS.GetText(10, 69, 7)).strip())
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=1)
                actividad.save(force_update=True)

                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return {
                    'estado': actividad.estadoDeSolicitud_id,
                    'mensaje': 'Solicitud creada correctamente',
                    'solicitud': actividad.numeroDeSolicitud,
                }

            else:
                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return self.ERROR
        else:
            return self.ERROR

    def pasoDos(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 12) == 'INSPECCIONES' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '8'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                pass
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 38) == 'IMPRESION DE FORMULARIOS DE INSPECCION' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PCLCUIMF'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '5'):
                    self.solicitudesNuevo = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    pass
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[eraseeof]', 8, 5)
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud), 8, 5)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('6')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=6)
                actividad.save(force_update=True)

                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return {
                    'estado': actividad.estadoDeSolicitud_id,
                    'mensaje': 'Solicitud enviada para impresion al servidor',
                    'solicitud': actividad.numeroDeSolicitud
                }
            else:
                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return self.ERROR
        else:
            return self.ERROR

    def pasoTres(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 12) == 'INSPECCIONES' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '8'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                pass
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 38) == 'DIGITAR PRIMERA INSPECCION' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PDIPRIN'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '20'):
                    self.solicitudesNuevo = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    pass
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud), 8, 6)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[eraseeof]')
                sesion.autECLPS.SendKeys(str(contrato.codigoInstalador),8,33)
                sesion.autECLPS.SendKeys('[pf4]', 9, 33)
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                ref=list(detalleClienteReferencia.objects.filter(cliente=actividad.cliente))[0].referencia
                meref=detalleClienteMedidor.objects.filter(
                    cliente=ref,
                    medidor__contrato=None,
                    medidor__actividad=actividad
                )[0].medidor
                sesion.autECLPS.SendKeys(str(meref.febrica), 5, 15)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                if str(sesion.autECLPS.GetText(16, 14, 11)).strip()==str(meref.febrica):
                    sesion.autECLPS.SendKeys('1')
                    sesion.autECLPS.SendKeys('[enter]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                else:
                    return self.ERROR

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('S', 7, 72)
                sesion.autECLPS.SendKeys(str(actividad.materialDeLaRed_id), 8, 30)
                sesion.autECLPS.SendKeys(str(actividad.estadoDeLaInstalacion_id), 9, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 10, 30)
                sesion.autECLPS.SendKeys(str(actividad.tipoDeConstruccion_id), 10, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 11, 30)
                sesion.autECLPS.SendKeys(str(actividad.ubicacionDelMedidor_id), 11, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 12, 30)
                sesion.autECLPS.SendKeys(str(actividad.tipoDeAcometidaRed_id), 12, 30)
                sesion.autECLPS.SendKeys(str(actividad.tipoDeAcometidaRed_id), 13, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 14, 30)
                sesion.autECLPS.SendKeys(str(actividad.calibreDeLaRed_id), 14, 30)
                sesion.autECLPS.SendKeys(str(actividad.claseRed_id), 15, 30)
                med = medidor.objects.get(actividad=actividad, contrato__contrato=self.contrato)
                sesion.autECLPS.SendKeys('1', 16, 30)
                if med.voltaje==120:
                    sesion.autECLPS.SendKeys('2', 16, 34)
                else:
                    sesion.autECLPS.SendKeys('3', 16, 34)
                sesion.autECLPS.SendKeys('B', 16, 38)
                sesion.autECLPS.SendKeys(str(actividad.usoDeEnergia_id), 17, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 18, 30)
                sesion.autECLPS.SendKeys('[eraseeof]', 18, 34)
                sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble_id), 18, 30)
                sesion.autECLPS.SendKeys(str(actividad.usoEspecificoDelInmueble.usoGeneral_id), 18, 34)
                sesion.autECLPS.SendKeys(str(actividad.nivelSocieconomico_id), 19, 30)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=7)
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
                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return self.ERROR
        else:
            return self.ERROR

    def pasoCuatro(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 12) == 'INSPECCIONES' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '8'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                pass
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 21) == 'ASIGNAR MATERIAL TIPO' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PESESOLI'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '40'):
                    self.solicitudesNuevo = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    pass
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[eraseeof]', 8, 6)
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud), 8, 6)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
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

                sesion.autECLPS.SendKeys('[pf3]')

                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=75)
                actividad.save(force_update=True)

                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return {
                    'estado': actividad.estadoDeSolicitud_id,
                    'mensaje': 'Materiales descargados para la actividad',
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return self.ERROR
        else:
            return self.ERROR

    def pasoCinco(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 12) == 'INSPECCIONES' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '8'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '50'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                pass
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 12)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 21) == 'ASIGNAR MATERIAL TIPO' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PESESOLI'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '40'):
                    self.solicitudesNuevo = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    pass
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[eraseeof]', 8, 6)
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud), 8, 6)
                sesion.autECLPS.SendKeys('[enter]')
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
                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return self.ERROR
        else:
            return self.ERROR

    def pasoSeis(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 23) == 'ATENCION DE SOLICITUDES' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '30'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '5'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                pass
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 25)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 21) == 'FACTURACION DE CONCEPTOS Y GARANTIAS - SERVICIO' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PFACSOL'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '20'):
                    self.solicitudesNuevo = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    pass
            if opcionSico:

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

                sesion.autECLPS.SendKeys('C', 5, 28)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[pf2]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('[eraseeof]', 8, 46)
                sesion.autECLPS.SendKeys('1', 8, 46)
                sesion.autECLPS.SendKeys('[eraseeof]', 10, 46)
                sesion.autECLPS.SendKeys('4', 10, 46)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=85)
                actividad.save(force_update=True)

                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return {
                    'estado': actividad.estadoDeSolicitud.id,
                    'mensaje': 'Garantia generada',
                    'solicitud': actividad.numeroDeSolicitud
                }

            else:
                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return self.ERROR
        else:
            return self.ERROR

    def pasoSiete(self, actividad):
        sesion = self.sesion
        opcionSico = False
        sesion.autECLPS.SetCursorPos(9, 12)
        for i in range(9, 20):
            if sesion.autECLPS.GetText(i, 16, 23) == 'CAJA VARIOS' \
                or (str(sesion.autECLPS.GetText(i, 52, 3)).strip() == '85'
                    and str(sesion.autECLPS.GetText(i, 63, 2)).strip() == '10'):
                self.cambiosDeMedidor = i
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                pass
        if opcionSico:

            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            opcionSico = False
            sesion.autECLPS.SetCursorPos(9, 25)
            for i in range(9, 20):
                if sesion.autECLPS.GetText(i, 7, 44) == 'RECAUDACIÓN DE FACTURAS GARANTÍAS E INGRESOS' \
                    or (str(sesion.autECLPS.GetText(i, 58, 8)).strip() == 'PRECOIN'
                        and str(sesion.autECLPS.GetText(i, 62, 2)).strip() == '10'):
                    self.solicitudesNuevo = i
                    sesion.autECLPS.SendKeys('1', i, 3)
                    opcionSico = True
                    break
                else:
                    pass
            if opcionSico:

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[pf7]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[eraseeof]', 8, 50)
                sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud), 8, 50)
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                sesion.autECLPS.SendKeys('7')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=9)
                actividad.save(force_update=True)

                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

                return {
                    'estado': actividad.estadoDeSolicitud.id,
                    'mensaje': 'Ejecutada reimpresión de grantía',
                    'solicitud': actividad.numeroDeSolicitud
                }


            else:
                titulo = sesion.autECLPS.GetText(9, 16, 20)
                while titulo != 'CONSULTA DE CLIENTES':
                    sesion.autECLPS.SendKeys('[pf12]')
                    sesion.autECLOIA.WaitForAppAvailable()
                    sesion.autECLOIA.WaitForInputReady()
                    titulo = sesion.autECLPS.GetText(9, 16, 20)

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
                sesion.autECLPS.SendKeys('5', i, 12)
                opcionSico = True
                break
            else:
                sesion.autECLPS.SendKeys('[down]')
        if opcionSico:

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

    def pasoOcho(self, actividad):
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
            sesion.autECLPS.SendKeys('[eraseeof]', 8, 32)
            sesion.autECLPS.SendKeys('1', 8, 32)
            sesion.autECLPS.SendKeys('[eraseeof]', 8, 35)
            sesion.autECLPS.SendKeys('2', 8, 35)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=10)
            actividad.save(force_update=True)

            titulo = sesion.autECLPS.GetText(9, 16, 20)
            while titulo != 'CONSULTA DE CLIENTES':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(9, 16, 20)

            return {
                'estado': actividad.estadoDeSolicitud_id,
                'mensaje': 'Generada solicitud a bodega...',
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            return self.ERROR

    def pasoNueve(self, actividad):
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

    def pasoDiez(self, actividad):
        if self.pasoAcceso():
            sesion = self.sesion
            sesion.autECLPS.SendKeys('5')
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            sesion.autECLPS.SendKeys('[eraseeof]')
            sesion.autECLPS.SendKeys(str(actividad.numeroDeSolicitud),9,7)
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

    def pasoOnce(self, actividad):
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

    def pasoDoce(self, actividad):
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

            titulo = sesion.autECLPS.GetText(9, 16, 20)
            while titulo != 'CONSULTA DE CLIENTES':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(9, 16, 20)

            return retorno

        else:
            return self.ERROR

    def pasoCatorce(self, actividad):
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

            sesion.autECLPS.SendKeys('3')    #454
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()

            #i = 10
            #f = str(sesion.autECLPS.GetText(i, 56, 10))
            #returno = self.ERROR
            #while f.strip() != '0/00/0000' or f.strip() != '00/00/0000':
            #    i += 1
            #
            #if i < 20:
            #    sesion.autECLPS.SendKeys('4', i, 4)
            #    sesion.autECLPS.SendKeys('[enter]')
            #    sesion.autECLOIA.WaitForAppAvailable()
            #    sesion.autECLOIA.WaitForInputReady()
            #    sesion.autECLPS.SendKeys('s')
            #    med = list(medidor.objects
            #    .filter(actividad__id=actividad.id)
            #    .exclude(contrato__contrato=self.contrato)
            #    )[0]
            #    sesion.autECLPS.SendKeys('[eraseeof]', 11, 70)
            #    sesion.autECLPS.SendKeys(str(med.lectura), 11, 70)
            #    sesion.autECLPS.SendKeys('[enter]')
            #    sesion.autECLOIA.WaitForAppAvailable()
            #    sesion.autECLOIA.WaitForInputReady()

            med=list(medidor.objects
            .filter(actividad__id=actividad.id, contrato__contrato=self.contrato)
            )[0]
            sesion.autECLPS.SendKeys(str(med.tipo)[:1], 6, 9)
            sesion.autECLPS.SendKeys(str(med.marca.id)[:3], 6, 13)
            sesion.autECLPS.SendKeys(str(med.fabrica), 6, 18)
            sesion.autECLPS.SendKeys('[enter]')
            sesion.autECLOIA.WaitForAppAvailable()
            sesion.autECLOIA.WaitForInputReady()
            returno=None
            if str(med.fabrica).strip() == str(sesion.autECLPS.GetText(7, 18, 12)).strip():
                sesion.autECLPS.SendKeys('1')
                sesion.autECLPS.SendKeys('[enter]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                sesion.autECLPS.SendKeys('S')
                sesion.autECLPS.SendKeys('[eraseeof]', 10, 62)
                sesion.autECLPS.SendKeys('00000', 10, 62)
                sesion.autECLPS.SendKeys('[pf2]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()

                actividad.estadoDeSolicitud = estadoDeSolicitud.objects.get(id=454)
                actividad.save(force_update=True)

                returno={
                    'estado': actividad.estadoDeSolicitud_id,
                    'mensaje': actividad.estadoDeSolicitud.descripcion,
                    'solicitud': actividad.numeroDeSolicitud
                }

            titulo = sesion.autECLPS.GetText(9, 16, 20)
            while titulo != 'CONSULTA DE CLIENTES':
                sesion.autECLPS.SendKeys('[pf12]')
                sesion.autECLOIA.WaitForAppAvailable()
                sesion.autECLOIA.WaitForInputReady()
                titulo = sesion.autECLPS.GetText(9, 16, 20)

            if returno:
                return returno
            else:
                return self.ERROR

        else:
            return self.ERROR

    def pasoQuince(self, actividad):
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

            medidorInst = list(medidor.objects.filter(actividad=actividad, contrato__contrato=self.contrato))[0]
            enlace = detalleClienteMedidor(
                lectura_instalacion = medidorInst.lectura,
                fecha_instalacion = now.date(),
                medidor = medidorInst,
                cliente = actividad.cliente
            )
            enlace.save()

            return {
                'estado': actividad.estadoDeSolicitud_id,
                'mensaje': actividad.estadoDeSolicitud.descripcion,
                'solicitud': actividad.numeroDeSolicitud
            }

        else:
            return self.ERROR