# WARNING: don't use logging in this module at all for performance!

from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtNetwork import QLocalSocket

import piony
from piony.system import logger


class Client:
    def __init__(self):
        self.socket = QLocalSocket()
        self.socket.setServerName(piony.G_SOCKET_NAME)
        self.socket.error.connect(self.displayError)
        self.socket.disconnected.connect(self.socket.deleteLater)

    def _log_(self, text, *args):
        logger.info(self.__class__.__qualname__ + ': ' + text, *args)

    def connect(self):
        self.socket.abort()
        self._log_("connection attempt")
        self.socket.connectToServer()

    def send(self, argv):
        data = QByteArray()
        out = QDataStream(data, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_5_0)
        out.writeQVariant(argv)
        self._log_("writes: %s", str(data))
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
        self._log_(msg)
