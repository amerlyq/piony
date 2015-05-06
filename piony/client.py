#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtNetwork import QLocalSocket

from piony.config.gvars import G_SOCKET_NAME
from piony.config.argparser import ArgsParser


class Client:
    def __init__(self):
        self.socket = QLocalSocket()
        self.socket.setServerName(G_SOCKET_NAME)
        self.socket.error.connect(self.displayError)
        self.socket.disconnected.connect(self.socket.deleteLater)
        print("Client: init")

    def connect(self):
        self.socket.abort()
        print("Client: connection attempt")
        self.socket.connectToServer()

    def send(self):
        Arg_Ps = ArgsParser()
        entries = vars(Arg_Ps.parse()).items()
        args = {k: v for k, v in entries if v}

        data = QByteArray()
        out = QDataStream(data, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_5_0)
        out.writeQVariant(args)

        print("Client writes:", data)
        self.socket.write(data)
        self.socket.flush()
        self.socket.disconnectFromServer()

    def displayError(self, err):
        errdesc = {
            QLocalSocket.ServerNotFoundError:
                "The host was not found. Check the host name and port.",
            QLocalSocket.ConnectionRefusedError:
                "The connection was refused by the peer. "
                "Check server is running, it's host and port.",
            QLocalSocket.PeerClosedError:
                "Peer was closed",  # None,
        }

        msg = errdesc.get(err, "Error occurred: {}."
                          .format(self.socket.errorString()))
        if msg is not None:
            print("Client:", msg)
