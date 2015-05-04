#!/usr/bin/env python3
# vim: fileencoding=utf-8

from sys import argv, exit
from signal import signal, SIGINT, SIG_DFL
from subprocess import check_output
from multiprocessing.connection import Listener, Client

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

import piony
from piony.config import cfgdefaults


def search_dst_window():
    out = check_output(['xdotool', 'getactivewindow'])
    idwnd = out[:-1].decode('ascii')
    return idwnd


def set_args_from_command_line(cfg, args):
    # print(vars(args))
    # print(getattr(args,'buds', None))
    cd = cfgdefaults.G_CONFIG_DEFAULT

    ar = {k: v for k, v in vars(args).items() if v}

    for section, opts in cd.items():
        for name_arg in list(ar):
            for name_arg_of_section in list(opts):
                if name_arg == name_arg_of_section:
                    cfg.set(section, name_arg, str(ar[name_arg]))
                    break

    # di = {'Window':{'size':88, 'aa':'bb'}}
    # cfg.read_dict(di)
    #
    # for s in cfg.sections():
    #     for o in cfg.options(s):
    #         print(s, o, cfg[s][o])


def sendArguments(path, auth):
    try:
        conn = Client(path, 'AF_UNIX', authkey=auth)
    except ConnectionRefusedError:
        import os
        os.remove(path)
    except FileNotFoundError:
        pass
    else:
        conn.send(argv)
        exit(0)


class Worker(QObject):
    finished = pyqtSignal()
    cfgChange = pyqtSignal()

    def __init__(self, path, auth):
        super().__init__()
        self.listener = Listener(path, 'AF_UNIX', authkey=auth)

    @pyqtSlot()
    def listenArguments(self):
        print("Listener")
        bListen = True
        while bListen:
            print("start")
            with self.listener.accept() as conn:
                print("conn")
                msg = conn.recv()
                if isinstance(msg, str):
                    if msg == "-k":
                        bListen = False
                        break
                elif isinstance(msg, list) and len(msg) > 1:
                    print(msg)
                    if msg[1] == "-k":
                        bListen = False
                    else:
                        self.cfgChange.emit()
        self.finished.emit()


def onCfgChange():
    print('cfgChange')
    # QApplication.instance().quit()


def loadConfig():
    ## Read configuration files
    # cdir = os.path.dirname(os.path.abspath(__file__))
    Arg_Ps = piony.ArgsParser()
    piony.gvars.G_ACTIVE_WINDOW = search_dst_window()

    cfg = piony.ConfigParser().read_file()
    args = Arg_Ps.parse()
    set_args_from_command_line(cfg, args)
    Arg_Ps.apply(args)

    entries = args.buds if args.buds else cfg['Bud']['default']
    bud = piony.BudParser().read_args(entries)
    return cfg, bud


if __name__ == '__main__':
    ## Close on 'Ctrl-C' system signal.
    ## WARNING: No cleanup (can't implement because of Qt).
    signal(SIGINT, SIG_DFL)

    ## Send args to listener if exist or create new one.
    path = '/tmp/' + piony.__appname__ + '.sock'  # OR: path = ('localhost', 6000)
    auth = b'piony-ipc'
    sendArguments(path, auth)

    ## Create window and main loop
    app = QApplication(argv)

    thread = QThread()
    obj = Worker(path, auth)
    obj.cfgChange.connect(onCfgChange)
    obj.moveToThread(thread)
    obj.finished.connect(thread.quit)

    thread.started.connect(obj.listenArguments)
    thread.finished.connect(app.exit)
    thread.start()

    wnd = piony.Window(*loadConfig())
    wnd.setWindowTitle("{} {}".format(piony.__appname__, piony.__version__))
    wnd.show()

    ret = app.exec_()
    exit(ret)
