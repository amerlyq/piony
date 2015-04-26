#!/usr/bin/env python3
# vim: fileencoding=utf-8

import math
from PyQt5 import QtCore, QtGui, QtWidgets

import piony.layout.pie as lpie
import piony.segment_button as segbtn
from piony.action import sendKey
from piony.hgevent import HGEvent
from piony import gvars


class Window(QtWidgets.QWidget, HGEvent):
    def __init__(self, bud, args):
        super().__init__()
        self.bM3 = False
        self.ppos = QtCore.QPoint()
        self.size_w = args.size
        self.r = (0.3 * self.size_w) // 2
        self.dr = (0.7 * self.size_w) // 2

        self.setWnd()
        self.setContent(bud, args.no_tooltip)
        self.resize(self.sizeHint())
        self.centerOnCursor()

    def R(self):
        return self.r + self.dr

    def sizeHint(self):
        return QtCore.QSize(self.size_w, self.size_w)

    def setWnd(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint
                            | QtCore.Qt.FramelessWindowHint
                            # | QtCore.Qt.X11BypassWindowManagerHint
                            )
        self.installEventFilter(self)
        self.setMouseTracking(True)

        # Context menu -- can be used to add new shortcuts "on the fly"
        aQuit = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                                  triggered=QtWidgets.QApplication.instance().quit)
        self.addAction(aQuit)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def setContent(self, bud, no_tooltip):
        if no_tooltip == False:
            QtWidgets.QToolTip.setFont(QtGui.QFont('Ubuntu', 12))
            self.setToolTip('Slice No=1 <i>Click at any empty space to close.</i>')

        playout = lpie.PieLayout(self.r, self.dr, 0)
        for segment in bud:
            btn = segbtn.SegmentButton(None, segment.name)
            if no_tooltip == False:
                btn.setToolTip(segment.tooltip)
            btn.clicked.connect(lambda b: sendKey(segment.action))
            playout.addWidget(btn)
        self.setLayout(playout)

    def drawName(self, p):
        p.setFont(QtGui.QFont('Ubuntu', 16))
        p.setPen(QtGui.QColor(100, 100, 100, 200))
        sz = self.frameGeometry().size()
        r = self.r / math.sqrt(2)
        tq = QtCore.QRect(sz.width()/2 - r, sz.height()/2 - r, 2*r, 2*r)
        p.drawText(tq, QtCore.Qt.AlignCenter, "krita")

    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)  # p.begin(self)
        if __debug__ and gvars.G_DEBUG_VISUALS:
            self.drawBkgr(p)
        # self.drawName(p)  # temporarily disabled
        p.end()

    """
    For i3wm in dual monitor mode will create window _only_ on active monitor.
    Even if mouse is hovering on another monitor now.
    """
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
            p.setPen(QtCore.Qt.NoPen)
            p.setBrush(QtGui.QColor(255, 255, 0, 50))
            p.drawEllipse(self.rect())

