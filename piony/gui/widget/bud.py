import inject
from math import sqrt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QRect

import piony
from piony.gui.widget import base
from piony.gui.layout.pie import PieLayout
from piony.gui.widget.segment import SegmentWidget
from piony.system.action import sendKey
from piony.gstate import GState


class BudWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wdg = None
        self.setLayout(QtWidgets.QStackedLayout())
        self.setStyleSheet("background:transparent")

    def refreshBuds(self):
        if self.wdg:
            self.layout().removeWidget(self.wdg)
            self.wdg.close()
        self.wdg = SliceWidget()
        self.layout().addWidget(self.wdg)
        # QObjectCleanupHandler().add(self.layout())
        # self.setCurrentWidget(wdg) to display the one you want.
        self.resize(self.sizeHint())


class SliceWidget(QtWidgets.QWidget):
    @inject.params(gs=GState)
    def __init__(self, gs=None, parent=None):
        super().__init__(parent)
        self.sty = gs.sty['Bud']
        self.cfg = gs.cfg
        self.setStyleSheet("background:transparent")

        self.name = gs.bud['slices'][0].get('name', "slice")  # None
        ring = gs.bud['slices'][0]['rings'][0]

        a = int(self.cfg['Window']['size'])
        self.r = (0.3 * a) // 2
        self.dr = (0.7 * a) // 2

        pie = PieLayout(self.cfg, self.r, self.dr, 0)
        for segment in ring['segments']:
            btn = SegmentWidget(segment.name,
                                lambda a=segment.action: sendKey(a))
            if not bool(self.cfg['Window']['no_tooltip']):
                btn.setToolTip(segment.tooltip)
            pie.addWidget(btn)
        self.setLayout(pie)

        self.setFont(QtGui.QFont('Ubuntu', 16))

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

        a = min(self.width(), self.height())
        qr = QtCore.QRect(self.width()/2 - a/2, self.height()/2 - a/2, a, a)
        rgn = QtGui.QRegion(qr, QtGui.QRegion.Ellipse)
        self.setMask(rgn)

    ## --------------
    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)

        if __debug__ and piony.G_DEBUG_VISUALS:
            self._drawBkgr(p)
            self._drawMask(p)

        self.drawName(p)
        p.end()

    def drawName(self, p):
        a = self.r * sqrt(2)
        sz = self.frameGeometry().size()
        tq = QRect(sz.width()/2 - a/2, sz.height()/2 - a/2, a, a)
        ## text_scale -- has effect only untill you fit bbox
        tsz = tq.size() * float(self.sty['Text']['scale'])
        base.adjustFontSize(self, self.name, tsz)

        p.setPen(QtGui.QColor(*list(self.sty['Text']['color'])))
        p.drawText(tq, Qt.AlignCenter, self.name)

    ## --------------
    if __debug__:
        def _drawBkgr(self, p):
            p.setPen(QtCore.Qt.NoPen)
            p.setBrush(QtGui.QColor(0, 255, 255, 50))
            p.drawRect(self.geometry())

        def _drawMask(self, p):
            p.setPen(Qt.NoPen)
            p.setBrush(QtGui.QColor(255, 255, 0, 80))
            path = QtGui.QPainterPath()
            path.addRegion(self.mask())
            p.drawPath(path)
