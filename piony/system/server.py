from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtCore import QObject, QDataStream, pyqtSignal

import piony
from piony import logger
from piony.system import action


class Server(QObject):
    dataReceived = pyqtSignal(list)
    quit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.conn = None
        self.server = None

    def create(self, name=piony.G_SOCKET_NAME):
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
        logger.info("1 new conn")
        # WARNING: when multiple connections, each will overwrite previous!
        self.conn = self.server.nextPendingConnection()
        self.conn.readyRead.connect(self.receiveData)
        self.conn.disconnected.connect(self.conn.deleteLater)

    def receiveData(self):
        logger.info("Server: waits for data")
        ins = QDataStream(self.conn)
        ins.setVersion(QDataStream.Qt_5_0)
        if ins.atEnd():
            return
        argv = ins.readQVariant()
        logger.info("Server reads: %s", str(argv))
        # Must be setted up on 'show' action. Move from beginning to appropriate.
        action.search_dst_window()
        self.dataReceived.emit(argv)
