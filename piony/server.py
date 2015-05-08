#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtCore import QObject, QDataStream, pyqtSignal

from piony.config import gvars
from piony.config.load import stateLoader
from configparser import ConfigParser


class Server(QObject):
    dataReceived = pyqtSignal(ConfigParser, dict, bool)

    def __init__(self):
        super().__init__()
        self.cfg = None
        self.buds = None

        QLocalServer.removeServer(gvars.G_SOCKET_NAME)
        self.server = QLocalServer()
        if not self.server.listen(gvars.G_SOCKET_NAME):
            print("Error: server -- unable to start: {}."
                  .format(self.server.errorString()))
            # QApplication.instance().quit(); return
            exit(1)
        self.server.newConnection.connect(self.notify)
        self.conn = None

    def notify(self):
        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server: 1 new conn")
        # WARNING: when multiple connections, each will overwrite previous!
        self.conn = self.server.nextPendingConnection()
        self.conn.readyRead.connect(self.readData)
        self.conn.disconnected.connect(self.conn.deleteLater)

    def readData(self):
        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server: waits for data")

        ins = QDataStream(self.conn)
        ins.setVersion(QDataStream.Qt_5_0)
        if ins.atEnd():
            return
        args = ins.readQVariant()

        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server reads:", args)

        self.loadData(args)

    def loadData(self, args):
        self.cfg, self.buds = stateLoader()
        # TODO: Make 'bReload' as tuple to distinguish necessary refreshes.
        bReload = True if args.get('args', None) else False
        self.dataReceived.emit(self.cfg, self.buds, bReload)
