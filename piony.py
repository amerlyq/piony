#!/usr/bin/env python3
# vim: fileencoding=utf-8

# http://pyqt.sourceforge.net/Docs/PyQt4/qmouseevent.html

import sys, os
from piony import *
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # names = [ 'f', 'c','b','a', 'd', '0','.','=']
    # names = ['a','b','c','d']
    names = [ c for c in char_range('a','m') ]

    wnd = Window(names)
    wnd.show()
    sys.exit(app.exec_())

    ## For debug when working inside project/build/
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # args = mmm.cmd_args()

    # mmc = mmm.MMConvertor()
    # mmc.read(os.path.abspath(args.input))
    # for f_out in args.output:
    #     mmc.write(os.path.abspath(f_out))
    # mmc.write('out.stdio', type=None if 'auto' == args.oftype else args.oftype)
