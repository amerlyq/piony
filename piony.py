#!/usr/bin/env python3
# vim: fileencoding=utf-8

import sys

if __name__ == '__main__':

    ## Send args to listener and close
    from piony.system.client import Client
    client = Client()
    client.connect()
    if client.socket.waitForConnected(2000):
        client.send(sys.argv[1:])
        client.socket.close()

    else:
        ## Close on 'Ctrl-C' system signal.
        ## WARNING: No cleanup possible (can't implement because of Qt).
        from signal import signal, SIGINT, SIG_DFL
        signal(SIGINT, SIG_DFL)
        ## Create window and listening server
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)

        from piony.system.server import Server
        server = Server()
        server.quit.connect(app.quit)
        app.aboutToQuit.connect(server.close)
        server.create()

        from piony.window import Window
        wnd = Window()
        server.dataReceived.connect(wnd.reload)

        server.loadData(sys.argv[1:])
        sys.exit(app.exec_())
