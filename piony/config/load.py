#!/usr/bin/env python3
# vim: fileencoding=utf-8


def search_dst_window():
    from subprocess import check_output
    out = check_output(['xdotool', 'getactivewindow'])
    idwnd = out[:-1].decode('ascii')
    return idwnd


def set_args_from_command_line(cfg, args):
    from piony.config import cfgdefaults
    cd = cfgdefaults.G_CONFIG_DEFAULT

    ar = [(k, v) for k, v in vars(args).items() if v]

    for section, opts in cd.items():
        for k, v in ar:
            if k in opts:
                cfg.set(section, k, str(v))


def stateLoader():
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
