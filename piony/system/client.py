# WARNING: don't use logging in this module at all for performance!

from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtNetwork import QLocalSocket

import piony
from piony import logger


class Client:
    def __init__(self):
        self.socket = QLocalSocket()
        self.socket.setServerName(piony.G_SOCKET_NAME)
        self.socket.error.connect(self.displayError)
        self.socket.disconnected.connect(self.socket.deleteLater)

    def connect(self):
        self.socket.abort()
        logger.info("Client: connection attempt")
        self.socket.connectToServer()

    def send(self, argv):
        data = QByteArray()
        out = QDataStream(data, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_5_0)
        out.writeQVariant(argv)
        logger.info("Client writes: %s", str(data))
        self.socket.write(data)
        self.socket.flush()
        self.socket.disconnectFromServer()

    def displayError(self, err):
        msg = {
            QLocalSocket.ServerNotFoundError:
                "The host was not found. Check the host name and port.",
            QLocalSocket.ConnectionRefusedError:
                "The connection was refused by the peer. "
                "Check server is running, it's host and port.",
            QLocalSocket.PeerClosedError:
                "Peer was closed",  # None,
        }.get(err, "Client error: {}.".format(self.socket.errorString()))
        logger.info(msg)
