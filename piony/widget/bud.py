#!/usr/bin/env python3
# vim: fileencoding=utf-8

from math import sqrt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QRect

from piony.config import gvars
from piony.widget import base
from piony.action import sendKey
from piony.layout.pie import PieLayout
from piony.widget.segment import SegmentWidget


class BudWidget(QtWidgets.QWidget):
    def __init__(self, bud, cfg, parent=None):
        super().__init__(parent)
        self.cfg = cfg

        self.name = bud['slices'][0].get('name', "slice")  # None
        ring = bud['slices'][0]['rings'][0]

        a = self.cfg['Window'].getint('size')
        self.r = (0.3 * a) // 2
        self.dr = (0.7 * a) // 2

        pie = PieLayout(self.cfg, self.r, self.dr, 0)
        for segment in ring['segments']:
            btn = SegmentWidget(self.cfg['Button'], segment.name,
                                lambda a=segment.action: sendKey(a))
            if not self.cfg['Window'].getboolean('no_tooltip'):
                btn.setToolTip(segment.tooltip)
            pie.addWidget(btn)
        self.setLayout(pie)

        self.setFont(QtGui.QFont('Ubuntu', 16))
        self.setMinimumSize(40, 40)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    ## --------------
    def minimalSize(self):
        return QSize(10, 10)

    def sizeHint(self):
        return QSize(2*base.R(self), 2*base.R(self))

    def setGeometry(self, rect):    # rect -- w/o margin
        super().setGeometry(rect)   # Necessary for updating masks and own geometry
        self.layout().setGeometry(rect)
        self.r = self.layout().r
        self.dr = self.layout().dr

        ## text_scale -- has effect only untill you fit bbox
        txtw = self.r * self.cfg['Bud'].getfloat('text_scale')
        base.adjustFontSize(self, self.name, QSize(txtw, txtw))

        a = min(self.width(), self.height())
        qr = QtCore.QRect(self.width()/2 - a/2, self.height()/2 - a/2, a, a)
        rgn = QtGui.QRegion(qr, QtGui.QRegion.Ellipse)
        self.setMask(rgn)

    ## --------------
    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)

        if __debug__ and gvars.G_DEBUG_VISUALS:
            self.drawBkgr(p)
            self.drawMask(p)

        self.drawName(p)
        p.end()

    def drawName(self, p):
        a = self.r * sqrt(2)
        sz = self.frameGeometry().size()
        tq = QRect(sz.width()/2 - a/2, sz.height()/2 - a/2, a, a)

        p.setPen(QtGui.QColor(100, 100, 100, 200))
        p.drawText(tq, Qt.AlignCenter, self.name)

    ## --------------
    if __debug__:
        def drawBkgr(self, p):
            p.setPen(QtCore.Qt.NoPen)
            p.setBrush(QtGui.QColor(0, 255, 255, 50))
            p.drawRect(self.geometry())

        def drawMask(self, p):
            p.setPen(Qt.NoPen)
            p.setBrush(QtGui.QColor(255, 255, 0, 80))
            path = QtGui.QPainterPath()
            path.addRegion(self.mask())
            p.drawPath(path)
