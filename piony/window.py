#!/usr/bin/env python3
# vim: fileencoding=utf-8

import math
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QSize, QRect

from piony.layout.pie import PieLayout
from piony.segment_button import SegmentButton
from piony.action import sendKey
from piony.hgevent import HGEventMixin
from piony import gvars


class Window(QtWidgets.QWidget, HGEventMixin):
    def __init__(self, cfg, bud):
        super().__init__()
        self.cfg = cfg
        self.opts = self.cfg['Window']
        self.bM3 = False
        self.ppos = QPoint()
        self.size_w = cfg['Window'].getint('size')
        self.r = (0.3 * self.size_w) // 2
        self.dr = (0.7 * self.size_w) // 2

        self.setWnd()
        self.setContent(bud, not self.cfg['Window'].getboolean('no_tooltip'))
        self.resize(self.sizeHint())
        self.centerOnCursor()

    def R(self):
        return self.r + self.dr

    def sizeHint(self):
        return QSize(self.size_w, self.size_w)

    def setWnd(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        wflags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        # if not __debug__:
        #     wflags |= Qt.X11BypassWindowManagerHint
        self.setWindowFlags(wflags)
        self.installEventFilter(self)
        self.setMouseTracking(True)

        # Context menu -- can be used to add new shortcuts "on the fly"
        aQuit = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                                  triggered=QtWidgets.QApplication.instance().quit)
        self.addAction(aQuit)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def setContent(self, bud, has_tooltip):
        if has_tooltip:
            QtWidgets.QToolTip.setFont(QtGui.QFont('Ubuntu', 12))
            self.setToolTip('Slice No=1 <i>Click at any empty space to close.</i>')

        playout = PieLayout(self.r, self.dr, 0)
        for segment in bud:
            btn = SegmentButton(self.cfg['Button'], segment.name,
                                lambda a=segment.action: sendKey(a))
            if has_tooltip:
                btn.setToolTip(segment.tooltip)
            playout.addWidget(btn)
        self.setLayout(playout)

    def drawName(self, p):
        p.setFont(QtGui.QFont('Ubuntu', 16))
        p.setPen(QtGui.QColor(100, 100, 100, 200))
        sz = self.frameGeometry().size()
        r = self.r / math.sqrt(2)
        tq = QRect(sz.width()/2 - r, sz.height()/2 - r, 2*r, 2*r)
        p.drawText(tq, Qt.AlignCenter, "krita")

    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)  # p.begin(self)
        if __debug__ and gvars.G_DEBUG_VISUALS:
            self.drawBkgr(p)
        # self.drawName(p)  # temporarily disabled
        p.end()

    def centerOnCursor(self):
        fg = self.frameGeometry()
        cp = QtGui.QCursor.pos()
        # cp = QtGui.QApplication.desktop().cursor().pos()
        # screen = QtGui.QApplication.desktop().screenNumber(cp)
        # sg = QtGui.QApplication.desktop().screenGeometry(screen)
        fg.moveCenter(cp)
        self.move(fg.topLeft())  # self.setGeometry(fg)

    if __debug__:
        def drawBkgr(self, p):
            p.setPen(Qt.NoPen)
            p.setBrush(QtGui.QColor(255, 255, 0, 50))
            p.drawEllipse(self.rect())
