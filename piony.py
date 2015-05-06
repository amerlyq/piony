#!/usr/bin/env python3
# vim: fileencoding=utf-8


def search_dst_window():
    from subprocess import check_output
    out = check_output(['xdotool', 'getactivewindow'])
    idwnd = out[:-1].decode('ascii')
    return idwnd


def set_args_from_command_line(cfg, args):
    # print(vars(args))
    # print(getattr(args,'buds', None))
    from piony.config import cfgdefaults
    cd = cfgdefaults.G_CONFIG_DEFAULT

    ar = [(k, v) for k, v in vars(args).items() if v]

    for section, opts in cd.items():
        for k, v in ar:
            if k in opts:
                cfg.set(section, k, str(v))

    # di = {'Window':{'size':88, 'aa':'bb'}}
    # cfg.read_dict(di)
    #
    # for s in cfg.sections():
    #     for o in cfg.options(s):
    #         print(s, o, cfg[s][o])


def loadConfig():
    ## Read configuration files
    # cdir = os.path.dirname(os.path.abspath(__file__))
    from piony.config import gvars
    from piony.config.cfgparser import ConfigParser
    from piony.config.argparser import ArgsParser
    from piony.config.budparser import BudParser
    gvars.G_ACTIVE_WINDOW = search_dst_window()

    Arg_Ps = ArgsParser()
    cfg = ConfigParser().read_file()
    args = Arg_Ps.parse()
    set_args_from_command_line(cfg, args)
    Arg_Ps.apply(args)

    entries = args.buds if args.buds else cfg['Bud']['default']
    bud = BudParser().read_args(entries)
    return cfg, bud


if __name__ == '__main__':
    ## Close on 'Ctrl-C' system signal.
    ## WARNING: No cleanup possible (can't implement because of Qt).
    from signal import signal, SIGINT, SIG_DFL
    signal(SIGINT, SIG_DFL)

    ## Send args to listener and close
    from piony.client import Client
    client = Client()
    client.connect()
    if client.socket.waitForConnected(2000):
        client.send()
        client.socket.close()
    else:
        ## Create window and listening server
        import sys
        from PyQt5.QtWidgets import QApplication
        from piony.server import Server
        from piony.window import Window
        import piony
        app = QApplication(sys.argv)
        server = Server()
        app.aboutToQuit.connect(server.server.close)

        wnd = Window(*loadConfig())
        wnd.setWindowTitle("{} {}".format(piony.__appname__, piony.__version__))
        wnd.show()
        sys.exit(app.exec_())
