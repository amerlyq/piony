#!/usr/bin/env python3
# vim: fileencoding=utf-8

import os
import sys
import json
from PyQt5.QtWidgets import QApplication

from piony import *
from piony import __appname__


if __name__ == '__main__':
    cdir = os.path.dirname(os.path.abspath(__file__))
    args = cmd_args()

    # mmc.read(os.path.abspath(args.input))
    # for f_out in args.output:
    #     mmc.write(os.path.abspath(f_out))
    # mmc.write('out.stdio', type=None if 'auto' == args.oftype else args.oftype)

    app = QApplication(sys.argv)

    # bud = [ c for c in char_range('a','m') ]
    with open('cfgs/map.json') as bud_file:
        bud = json.load(bud_file)

    wnd = Window(bud)
    wnd.setWindowTitle(__appname__)
    wnd.show()
    sys.exit(app.exec_())

