#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

import piony
from piony.widget.bud import BudWidget
from piony.hgevent import HGEventMixin


class Window(QtWidgets.QWidget, HGEventMixin):
    def __init__(self):
        super().__init__()
        self.setWnd()

    def setWnd(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        wflags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        # if not __debug__:
        #     wflags |= Qt.X11BypassWindowManagerHint
        self.setWindowFlags(wflags)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setWindowTitle("{} {}".format(piony.__appname__,
                                           piony.__version__))

    ## --------------
    def reload(self, cfg, buds, bReload):
        if not bReload:
            self.setVisible(not self.isVisible())
        else:
            self.cfg = cfg
            self.bud = BudWidget(buds, self.cfg, self)
            self.setContent()
            self.resize(self.sizeHint())
            # NOTE: don't forget to delete, or --hide will not work later
            self.show()

        self.centerOnCursor()

    def setContent(self):
        if self.cfg['Window'].getboolean('no_tooltip'):
            self.setToolTip(None)
        else:
            QtWidgets.QToolTip.setFont(QtGui.QFont('Ubuntu', 12))
            self.setToolTip('Slice No=1 <i>Click at any empty space to close.</i>')

        aQuit = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                                  triggered=QtWidgets.QApplication.instance().quit)
        self.addAction(aQuit)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    ## --------------
    def sizeHint(self):
        return self.bud.sizeHint()

    def minimumSize(self):
        return self.bud.minimalSize()

    def centerOnCursor(self):
        fg = self.frameGeometry()
        cp = QtGui.QCursor.pos()
        # cp = QtGui.QApplication.desktop().cursor().pos()
        # screen = QtGui.QApplication.desktop().screenNumber(cp)
        # sg = QtGui.QApplication.desktop().screenGeometry(screen)
        fg.moveCenter(cp)
        self.move(fg.topLeft())  # self.setGeometry(fg)

    ## --------------
    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)  # p.begin(self)
        self.drawCleanBkgr(p)
        p.end()

    def drawCleanBkgr(self, p):
        p.setPen(Qt.NoPen)
        p.setBrush(QtGui.QColor(0, 0, 0, 0))
        p.drawRect(self.rect())
