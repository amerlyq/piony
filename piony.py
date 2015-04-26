#!/usr/bin/env python3
# vim: fileencoding=utf-8

import os
import sys
import json
from PyQt5.QtWidgets import QApplication

import piony
from piony import gvars


def apply_args(args):
    if args.verbose == 'l':
        gvars.G_DEBUG_VISUALS = True
        gvars.G_DEBUG_ACTIONS = True
    elif args.verbose == 'v':
        gvars.G_DEBUG_VISUALS = True
        gvars.G_DEBUG_ACTIONS = False
    elif args.verbose == 'a':
        gvars.G_DEBUG_VISUALS = False
        gvars.G_DEBUG_ACTIONS = True

if __name__ == '__main__':
    cdir = os.path.dirname(os.path.abspath(__file__))
    args = piony.cmd_args()

    # mmc.read(os.path.abspath(args.input))
    # for f_out in args.output:
    #     mmc.write(os.path.abspath(f_out))
    # mmc.write('out.stdio', type=None if 'auto' == args.oftype else args.oftype)

    # cfg = [ c for c in char_range('a','m') ]
    with open('cfgs/map.json') as cfg_file:
        cfg = json.load(cfg_file)
    bud = piony.CfgParse().parse(cfg)

    apply_args(args)

    app = QApplication(sys.argv)
    wnd = piony.Window(bud, args.size)
    wnd.setWindowTitle(piony.__appname__)
    wnd.show()
    sys.exit(app.exec_())
