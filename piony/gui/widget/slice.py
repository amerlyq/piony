from math import sqrt

import inject
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (QGraphicsWidget, QGraphicsLinearLayout,
                             QStylePainter)

import piony
from piony.gui import logger
from piony.gstate import GState
from piony.gui.widget import base
from piony.gui.widget.segment import SegmentWidget
from piony.system.action import sendKey


class SliceWidget(QGraphicsWidget):
    @inject.params(gs=GState)
    def __init__(self, gs=None, parent=None):
        logger.info('%s init', self.__class__.__qualname__)
        super().__init__(parent)
        self.sty = gs.sty['Bud']
        self.cfg = gs.cfg

        self.name = gs.bud['slices'][0].get('name', "slice")  # None
        ring = gs.bud['slices'][0]['rings'][0]

        a = int(self.cfg['Window']['size'])
        self.r = (0.3 * a) // 2
        self.dr = (0.7 * a) // 2

        # ringLayout = RingLayout(self.cfg, self.r, self.dr, 0)
        ringLayout = QGraphicsLinearLayout()
        for segment in ring['segments']:
            btn = SegmentWidget(segment.name,
                                lambda a=segment.action: sendKey(a))
            if not bool(self.cfg['Window']['no_tooltip']):
                btn.setToolTip(segment.tooltip)
            ringLayout.addItem(btn)
        self.setLayout(ringLayout)

        self.setFont(QtGui.QFont('Ubuntu', 16))

    ## --------------
    def paintEvent(self, e):
        p = QStylePainter(self)

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
            p.setPen(Qt.NoPen)
            p.setBrush(QtGui.QColor(0, 255, 255, 50))
            p.drawRect(self.geometry())

        def _drawMask(self, p):
            p.setPen(Qt.NoPen)
            p.setBrush(QtGui.QColor(255, 255, 0, 80))
            path = QtGui.QPainterPath()
            path.addRegion(self.mask())
            p.drawPath(path)
