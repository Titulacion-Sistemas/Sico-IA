import pythoncom

__author__ = 'Jhonsson'
from time import sleep
import win32com
import win32com.client


class manejadorDeConexion:
    def __init__(self):
        pythoncom.CoInitialize()
        self.PCommConnMgr = win32com.client.Dispatch('PCOMM.autECLConnMgr')
        self.connList = self.PCommConnMgr.autECLConnList
        self.activeSession = None
        self.activeConnection = ''
        self.estado = False


    def setActiveSession(self, connectionName):
        self.activeSession = win32com.client.Dispatch("PCOMM.autECLSession")
        if connectionName:
            self.activeConnection = connectionName
        self.activeSession.SetConnectionByName(self.activeConnection)

        # return value from screen at position (row, col)


    def getText(self, row, col, length=None, connectionName=None):
        if connectionName is not None:
            self.setActiveSession(connectionName)

        if length is None:
            self.activeSession.autECLPS.autECLFieldList.Refresh()
            field = self.activeSession.autECLPS.autECLFieldList.FindFieldByRowCol(row, col)
            length = field.Length
        result = self.activeSession.autECLPS.GetText(row, col, length)
        return result


    def sendKeys(self, count, key, row=None, col=None, connectionName=None, wait=True):
        n = 0
        if connectionName is not None:
            self.setActiveSession(connectionName)

        while n < count:
            if row is None or col is None:
                self.activeSession.autECLPS.SendKeys("%s" % key)
            else:
                self.activeSession.autECLPS.SendKeys("%s" % key, row, col)
            if wait:
                if not self.activeSession.autECLOIA.WaitForAppAvailable(5000): return False
                if not self.activeSession.autECLOIA.WaitForInputReady(5000): return False
            n += 1
        return True


    def getAvailableConnection(self):
        self.connList.Refresh()
        letra = 65
        #self.activeConnection = chr(self.connList.Count + 65)
        v = self.connList.FindConnectionByName(chr(letra))

        while v is not None:
            print v
            letra += 1
            v = self.connList.FindConnectionByName(chr(letra))

        self.activeConnection = chr(letra)
        return self.activeConnection


    def openSession(self, connectionName=None, usuario="none", contrasenia="none"):

        self.estado = False

        if connectionName is not None:
            self.setActiveSession(connectionName)
        else:
            self.setActiveSession(self.getAvailableConnection())

        segundos = 40

        while not self.activeSession.Ready and segundos >= 0:
            print "la session no esta lista aun ..."
            #return False
            sleep(1)
            segundos -= 1

        if segundos >= 0:
            if self.activeSession.autECLOIA.WaitForAppAvailable(5000):
                if self.activeSession.autECLOIA.WaitForInputReady(5000):
                    print self.getText(22, 50, length=8)
                    print self.getText(21, 50, length=12)

            if self.activeSession.autECLPS.WaitForString('USUARIO', 21, 50, 10000):
                if self.sendKeys(1, usuario, row=21, col=63):
                    if self.sendKeys(1, contrasenia, row=22, col=63):

                        titulo = self.activeSession.autECLPS.GetText(5, 1, 11)
                        print 'Intentando acceder a Pantalla Principal...'
                        while titulo != '5=Programas' \
                            and segundos >= 0 \
                            and self.getText(24, 1, length=1) == " ":
                            self.activeSession.autECLPS.SendKeys('[enter]')
                            self.activeSession.autECLOIA.WaitForAppAvailable()
                            self.activeSession.autECLOIA.WaitForInputReady()
                            segundos -= 1
                            titulo = self.activeSession.autECLPS.GetText(5, 1, 11)

                        if titulo == '5=Programas':
                            self.estado = True
                            return self.estado
                        elif self.getText(24, 1, length=1) != " ":
                            self.estado = (self.getText(24, 1, length=75)).encode('utf-8').strip()
                        elif self.getText(1, 25, length=16) == "INICIO DE SESION":
                            self.estado = "Usuario incorrecto..."

        self.closeProgram(self.activeConnection, directo=True)

        return self.estado


    def openProgram(self):
        print "Abriendo el Programa, Sesion: {0}".format(self.activeConnection)
        self.PCommConnMgr.StartConnection(
            "PROFILE=.\Sico_IA\pComm\sico\CNEL.WS CONNNAME={0} WINSTATE=MIN".format(self.activeConnection))


    def closeProgram(self, connection, directo=False):
        if not connection:
            connection = self.activeConnection
        try:
            print "Cerrando el Programa, Sesion: {0}".format(connection)
            if not directo:
                if not self.activeSession:
                    self.setActiveSession(connection)
                self.sendKeys(10, '[pf12]', connectionName=connection, wait=False)
            self.PCommConnMgr.StopConnection(connection, "saveprofile=no")
        except:
            print "No se ha podido cerrar la sesion: {0}".format(connection)