#!/usr/bin/env python3
# vim: fileencoding=utf-8

from sys import argv, exit
from signal import signal, SIGINT, SIG_DFL
from subprocess import check_output
from multiprocessing import Process, Value
from multiprocessing.connection import Listener, Client

from PyQt5.QtWidgets import QApplication

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


def listenArguments(bListen, listener, wnd):
    # = ['kill'] & ['no-daemon']
    while bListen.value:
        with listener.accept() as conn:
            msg = conn.recv()
            if isinstance(msg, str):
                if msg == "-k":
                    bListen.value = 0
                    break
            elif isinstance(msg, list) and len(msg) > 1:
                print(msg)
                if msg[1] == "-k":
                    bListen.value = 0
                    wnd.close()
    print("s",bListen.value)


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
    wnd = piony.Window(*loadConfig())
    wnd.setWindowTitle("{} {}".format(piony.__appname__, piony.__version__))
    wnd.show()

    bListen = Value('i', 1)
    listener = Listener(path, 'AF_UNIX', authkey=auth)
    pr = Process(target=listenArguments, args=(bListen, listener, wnd))
    pr.start()

    ret = app.exec_()

    print("hi", bListen.value)

    ## Close listener
    if bListen.value:
        print("ipc")
        with Client(path, 'AF_UNIX', authkey=auth) as conn:
            conn.send("-k")
    pr.join()
    exit(ret)
