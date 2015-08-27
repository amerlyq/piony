import inject
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QSize, QRect

from piony.config import gvars
from piony.widget import base
from piony.gstate import GState


class SegmentWidget(QtWidgets.QToolButton):
    gs = inject.attr(GState)

    def __init__(self, name="", act=None, parent=None):
        super().__init__(parent)
        self.sty = self.gs.sty['Segment']

        self.setText(name)
        self.action = act

        self.bHover = False
        self.bHold = False
        self.gPath = None
        self.gText = QRect(0, 0, 20, 20)

        self.setFont(QtGui.QFont('Ubuntu', 16))
        self.setMouseTracking(True)
        self.resize(self.sizeHint())
        # self.setMask(QtGui.QRegion(rct))

    ## --------------

    def minimalSize(self):
        return QSize(10, 10)

    def sizeHint(self):
        return QSize(80, 80)

    def enterEvent(self, e):
        # self.setStyleSheet("background-color:#45b545;")
        self.bHover = True

    def leaveEvent(self, e):
        # self.setStyleSheet("background-color:yellow;")
        self.bHover = False
        self.bHold = False

    def mousePressEvent(self, e):
        # if e.button() == Qt.LeftButton and _hasModCtrl():
        self.bHold = True
        self.update()

    def mouseReleaseEvent(self, e):
        # if e.button() == Qt.LeftButton and not _hasModCtrl():
        self.bHold = False
        self.update()
        self.action()
        # action.sysClose()

    ## --------------

    def createPainter(self):
        p = QtWidgets.QStylePainter(self)
        p.setRenderHints(QtGui.QPainter.Antialiasing |
                         QtGui.QPainter.TextAntialiasing |
                         QtGui.QPainter.SmoothPixmapTransform |
                         QtGui.QPainter.HighQualityAntialiasing, True)
        return p

    def _clr(self, nm):
        if self.bHold:
            regime = "press"
        elif self.bHover:
            regime = "select"
        else:
            regime = "normal"
        return QtGui.QColor(*list(self.sty[nm]['color'][regime]))

    def drawSegment(self, p):
        p.setBrush(self._clr("Filler"))
        p.setPen(QtGui.QPen(self._clr("Border"),
                            self.sty['Border']['width'], Qt.SolidLine))
        p.drawPath(self.gPath)

    def drawSegmentText(self, p):
        ## RFC: Move to setGeometry. BUG: 'self' instead 'p' causes circular call
        sz = self.gText.size() * float(self.sty['Text']['scale'])
        base.adjustFontSize(p, self.text(), sz)

        p.setPen(self._clr("Text"))
        if __debug__ and gvars.G_DEBUG_VISUALS:
            p.drawRect(self.gText)
        p.drawText(self.gText, Qt.AlignCenter, self.text())

    def paintEvent(self, e):
        p = self.createPainter()
        if __debug__ and gvars.G_DEBUG_VISUALS:
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
            p.drawRect(QRect(QPoint(2, 2), self.size() - QSize(4, 4)))
