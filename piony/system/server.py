from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtCore import QObject, QDataStream, pyqtSignal

from piony.config import gvars


class Server(QObject):
    dataReceived = pyqtSignal(list)
    quit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.conn = None
        self.server = None

    def create(self, name=gvars.G_SOCKET_NAME):
        QLocalServer.removeServer(name)
        self.server = QLocalServer()
        if not self.server.listen(name):
            print("Error: server -- unable to start: {}."
                  .format(self.server.errorString()))
            self.quit.emit()
        self.server.newConnection.connect(self.notify)

    def close(self):
        self.server.close()

    def notify(self):
        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server: 1 new conn")
        # WARNING: when multiple connections, each will overwrite previous!
        self.conn = self.server.nextPendingConnection()
        self.conn.readyRead.connect(self.receiveData)
        self.conn.disconnected.connect(self.conn.deleteLater)

    def receiveData(self):
        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server: waits for data")

        ins = QDataStream(self.conn)
        ins.setVersion(QDataStream.Qt_5_0)
        if ins.atEnd():
            return
        argv = ins.readQVariant()

        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server reads:", argv)

        self.dataReceived.emit(argv)
