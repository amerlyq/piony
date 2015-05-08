#!/usr/bin/env python3
# vim: fileencoding=utf-8

if __name__ == '__main__':

    ## Send args to listener and close
    from piony.client import Client
    client = Client()
    client.connect()
    if client.socket.waitForConnected(2000):
        client.send()
        client.socket.close()

    else:
        ## Close on 'Ctrl-C' system signal.
        ## WARNING: No cleanup possible (can't implement because of Qt).
        from signal import signal, SIGINT, SIG_DFL
        signal(SIGINT, SIG_DFL)
        ## Create window and listening server
        import sys
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)

        from piony.server import Server
        server = Server()
        app.aboutToQuit.connect(server.server.close)

        from piony.window import Window
        wnd = Window()
        server.dataReceived.connect(wnd.reload)
        server.loadData({"args": '-S'})  # sys.argv

        sys.exit(app.exec_())
