#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5 import QtCore,QtGui,QtWidgets

from .action import sendKey
from .hgevent import HGEvent
from .layout.pie import *
from .segment_button import *
from piony import common


class Window(QtWidgets.QWidget, HGEvent):
    def __init__(self, bud, size_w):
        super().__init__()
        self.bM3 = False
        self.ppos = QtCore.QPoint()
        self.size_w = size_w
        self.r = int(0.3 * self.size_w / 2)
        self.dr = int(0.7 * self.size_w / 2)

        self.setWnd()
        self.setContent(bud)
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
            # | QtCore.Qt.X11BypassWindowManagerHint  # unfocused
            )
        self.installEventFilter(self)
        self.setMouseTracking(True)

        # Context menu -- can be used to add new shortcuts "on the fly"
        quitAction = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=QtWidgets.QApplication.instance().quit)
        self.addAction(quitAction)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def setContent(self, bud):
        # QtGui.QToolTip.setFont(QtGui.QFont('Ubuntu', 12))
        # self.setToolTip('This is a <b>QWidget</b> widget')

        playout = PieLayout(self.r, self.dr, 0)
        for segment in bud:
            if isinstance(segment, dict):
                action = segment.get('action', None)
                name = segment.get('name', action)
            else:
                name = segment
            btn = SegmentButton(None, name)
            # btn.setToolTip('Action -> <b>' + name + '</b>')
            btn.clicked.connect(lambda b: sendKey(name))
            playout.addWidget(btn)
        self.setLayout(playout)

        ## Disabled until label will not intercept mouse press
        # lbl = QtGui.QLabel("<b>krita</b>")
        # lbl.setAlignment(QtCore.Qt.AlignCenter)
        # lbl.setStyleSheet("color:yellow;")
        # lbl.setFont(QtGui.QFont('SansSerif', 10))
        # # makeClickable(lbl).connect(self.close)
        # self.grid.addWidget(lbl, *pos)

    def drawBkgr(self, p):
        p.setPen(QtCore.Qt.NoPen);
        p.setBrush(QtGui.QColor(255, 255, 0, 50));
        p.drawEllipse(self.rect());

    def drawName(self, p):
        p.setFont(QtGui.QFont('Ubuntu', 16))
        p.setPen(QtGui.QColor(100,100,100,200))
        sz = self.frameGeometry().size()
        r = self.r / math.sqrt(2)
        tq = QRect(sz.width()/2 - r, sz.height()/2 - r, 2*r, 2*r)
        p.drawText(tq, Qt.AlignCenter, "krita")

    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self) # p.begin(self)
        if common.G_DEBUG_VISUALS: self.drawBkgr(p)
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

