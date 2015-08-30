import inject
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QSizeF, QRect

import piony
from piony.gui import logger
from piony.gui.widget import base
from piony.gstate import GState


class SegmentWidget(QtWidgets.QGraphicsWidget):
    gs = inject.attr(GState)
    _fsm_regime = {'default': 'normal', 'normal': 'select',
                   'select': 'press', 'press': 'select'}

    def _clr(self, name):
        return QtGui.QColor(*list(self.sty[name]['color'][self.regime]))

    def __init__(self, name="", act=None, parent=None):
        logger.info('%s init: %s', self.__class__.__qualname__, name)
        super().__init__(parent)
        self.sty = self.gs.sty['Segment']

        self.text = name
        self.doAction = act
        self.regime = 'normal'

        self.gPath = None
        self.gText = QRect(0, 0, 20, 20)

        self.setFont(QtGui.QFont('Ubuntu', 16))
        # self.setMouseTracking(True)
        # self.resize(self.sizeHint())
        # self.setMask(QtGui.QRegion(rct))

    ## --------------

    def minimalSize(self):
        return QSizeF(10, 10)

    # def sizeHint(self):
    #     return QSizeF(80, 80)

    def enterEvent(self, e):
        self.regime = SegmentWidget._fsm_regime[self.regime]

    def leaveEvent(self, e):
        self.regime = SegmentWidget._fsm_regime['default']

    def mousePressEvent(self, e):
        # if e.button() == Qt.LeftButton and _hasModCtrl():
        self.regime = SegmentWidget._fsm_regime[self.regime]
        self.update()

    def mouseReleaseEvent(self, e):
        # if e.button() == Qt.LeftButton and not _hasModCtrl():
        self.regime = SegmentWidget._fsm_regime[self.regime]
        self.update()
        self.doAction()

    ## --------------

    def drawSegment(self, p):
        p.setBrush(self._clr("Filler"))
        p.setPen(QtGui.QPen(self._clr("Border"),
                            float(self.sty['Border']['width']), Qt.SolidLine))
        p.drawPath(self.gPath)

    def drawSegmentText(self, p):
        ## RFC: Move to setGeometry. BUG: 'self' instead 'p' causes circular call
        sz = self.gText.size() * float(self.sty['Text']['scale'])
        base.adjustFontSize(p, self.text, sz)

        p.setPen(self._clr("Text"))
        if __debug__ and piony.G_DEBUG_VISUALS:
            p.drawRect(self.gText)
        p.drawText(self.gText, Qt.AlignCenter, self.text)

    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)
        if __debug__ and piony.G_DEBUG_VISUALS:
            self.drawSegmentRegion(p)
        self.drawSegment(p)
        self.drawSegmentText(p)
        p.end()

    if __debug__:
        def drawSegmentRegion(self, p):  # Gradient brush
            grd = QtGui.QLinearGradient(0, 0, self.sizeHint().width(), 0)
            grd.setColorAt(0.0, QtGui.QColor(0, 0, 0, 40))
            grd.setColorAt(1.0, QtGui.QColor(0, 0, 0, 40))
            p.setBrush(grd)
            p.setPen(QtGui.QPen(Qt.NoPen))
            p.drawRect(QRect(QPoint(2, 2), self.size() - QSizeF(4, 4)))
