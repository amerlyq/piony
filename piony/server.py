#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtCore import QDataStream

from piony.config.gvars import G_SOCKET_NAME


class Server:
    def __init__(self):
        QLocalServer.removeServer(G_SOCKET_NAME)
        self.server = QLocalServer()
        if not self.server.listen(G_SOCKET_NAME):
            print("Server -- unable to start: {}."
                  .format(self.server.errorString()))
            # QApplication.instance().quit(); return
            exit(1)
        print("Server: listening")
        self.server.newConnection.connect(self.notify)
        self.conn = None

    def notify(self):
        print("1 new conn")
        # WARNING: when multiple connections, each will overwrite previous!
        self.conn = self.server.nextPendingConnection()
        self.conn.readyRead.connect(self.readData)
        self.conn.disconnected.connect(self.conn.deleteLater)

    def readData(self):
        print("Server: waits for data")

        ins = QDataStream(self.conn)
        ins.setVersion(QDataStream.Qt_5_0)
        if ins.atEnd():
            return

        args = ins.readQVariant()
        print("Server reads:", args)
