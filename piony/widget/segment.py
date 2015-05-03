#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QSize, QRect

from piony import gvars
from piony.widget import base


class PetalStyle():
    wLine = 3

    def __init__(self):
        self.cBorder = {"select": [255, 200, 0, 220],
                        "press": [255, 200, 0, 220],
                        "normal": [10, 10, 0, 220]}
        self.cFiller = {"select": [30, 30, 0, 180],
                        "press": [30, 80, 0, 180],
                        "normal": [40, 40, 40, 180]}  # 10, 10, 0
        self.cText = {"select": [255, 120, 0, 255],
                      "press": [255, 40, 40, 255],
                      "normal": [100, 255, 0, 255]}


class SegmentWidget(QtWidgets.QToolButton):
    def __init__(self, opts, name="", act=None, parent=None):
        super().__init__(parent)

        self.opts = opts
        self.setText(name)
        self.action = act

        self.text_scale = self.opts.getfloat('text_scale')

        self.bHover = False
        self.bHold = False
        self.gPath = None
        self.gText = QRect(0, 0, 20, 20)
        self.pstyle = PetalStyle()

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
            clr = "press"
        elif self.bHover:
            clr = "select"
        else:
            clr = "normal"
        return QtGui.QColor(*getattr(self.pstyle, nm)[clr])

    def drawSegment(self, p):
        p.setBrush(self._clr("cFiller"))
        p.setPen(QtGui.QPen(self._clr("cBorder"), PetalStyle.wLine, Qt.SolidLine))
        p.drawPath(self.gPath)

    def drawSegmentText(self, p):
        ## RFC: Move to setGeometry. BUG: 'self' instead 'p' causes circular call
        base.adjustFontSize(p, self.text(), self.gText.size())

        p.setPen(self._clr("cText"))
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
