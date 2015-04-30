#!/usr/bin/env python3
# vim: fileencoding=utf-8

import os
import sys
import signal
from subprocess import check_output
from PyQt5.QtWidgets import QApplication

import piony
from piony import gvars
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

if __name__ == '__main__':
    cdir = os.path.dirname(os.path.abspath(__file__))
    Cfg_Ps = piony.ConfigParser()
    Arg_Ps = piony.ArgsParser()
    Prf_Ps = piony.ProfileParser()
    gvars.G_ACTIVE_WINDOW = search_dst_window()

    cfg = Cfg_Ps.read_file()
    args = Arg_Ps.parse()
    set_args_from_command_line(cfg, args)
    Arg_Ps.apply(args)

    prfs = []
    for entry in args.buds:
        print(entry)
        if '-' == entry:
            entry = sys.stdin.read()
        elif os.path.isfile(entry):
            # os.path.isabs(PATH)
            with open(entry, 'r') as f:
                entry = f.read()
        # prfs.append(Prf_Ps.read_str(entry))

    bud = prfs[0] if prfs else Prf_Ps.read_file(cfg['Bud']['default'])

    ## Close on 'Ctrl-C' system signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    wnd = piony.Window(cfg, bud)
    wnd.setWindowTitle(piony.__appname__)
    wnd.show()
    sys.exit(app.exec_())
