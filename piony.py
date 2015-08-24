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
        from PyQt5.QtWidgets import QApplication
        from piony.window import MainApplication
        from signal import signal, SIGINT, SIG_DFL
        ## Close on 'Ctrl-C' system signal.
        ## WARNING: No cleanup possible (can't implement because of Qt).
        signal(SIGINT, SIG_DFL)
        app = QApplication(sys.argv)
        main = MainApplication(sys.argv)
        sys.exit(app.exec_())
