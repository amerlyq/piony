from math import sqrt

import inject
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (  # QGraphicsItem
    QGraphicsWidget, QGraphicsLinearLayout,  # QSizePolicy,
                             QStylePainter, QStyle)
from PyQt5.QtCore import Qt, QRect  # , QRectF

import piony
from piony.gui import logger
from piony.gui.widget import base
from piony.gui.layout.ring import RingLayout
from piony.gui.widget.segment import SegmentWidget
from piony.system.action import sendKey
from piony.gstate import GState


class MyItem(QGraphicsWidget):
    def __init__(self, clr):
        super().__init__()
        self.clr = clr
        # self.resize(80, 20)
        # self.setPos(0, 0)
        # self.setFlags(QGraphicsItem.ItemIsSelectable |
        #               QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return self.geometry()

    # def sizeHing(self):
    #     logger.info('%s hint %s', self.__class__.__qualname__, str(self.geometry()))
    #     return self.geometry()

    # def setGeometry(self, r):
    #     logger.info('%s setGeometry %s', self.__class__.__qualname__, str(r))
    #     super().setGeometry(r)

    # def mousePressEvent(self, e):
    #     self.setFocus()
    #     super().mousePressEvent(e)

    def paint(self, p, option, widget):
        pen = QtGui.QPen(Qt.black, 3, Qt.SolidLine)
        if option.state & QStyle.State_Selected:
            pen.setColor(Qt.yellow)
        p.setPen(pen)
        p.setBrush(self.clr)
        p.drawEllipse(option.rect)


class BudWidget(QGraphicsWidget):
    def __init__(self, parent=None):
        logger.info('%s init', self.__class__.__qualname__)
        super().__init__(parent)
        self.wdg = None
        # self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        hl = RingLayout()
        for clr in [Qt.red, Qt.green, Qt.blue,
                    QtGui.QColor(255, 255, 255, 40)]:
            item = MyItem(clr)
            logger.info('%s', str(item.geometry()))
            hl.addItem(item)

        self.setLayout(hl)
        # self.setLayout(QGraphicsLinearLayout())  # QStackedLayout
        # self.layout().addItem(QGraphicsEllipseItem(0, 0, 80, 40))
        # self.setStyleSheet("background:transparent")

    def refreshBuds(self):
        logger.info('%s: buds', self.__class__.__qualname__)
        pass
        # if self.wdg:
        #     self.layout().removeWidget(self.wdg)
        #     self.wdg.close()
        # self.wdg = SliceWidget()
        # self.layout().addItem(self.wdg)
        # QObjectCleanupHandler().add(self.layout())
        # self.setCurrentWidget(wdg) to display the one you want.
        # self.resize(self.sizeHint())

    def setGeometry(self, r):
        super().setGeometry(r)
        logger.info('%s setGeometry %s', self.__class__.__qualname__, str(self.geometry()))

    def resizeEvent(self, e):
        logger.info('%s: resize', self.__class__.__qualname__)
        super().resizeEvent(e)

    def paint(self, p, option, widget):
        p.setPen(QtGui.QPen(Qt.magenta, 3, Qt.SolidLine))
        p.drawRect(self.boundingRect())


class SliceWidget(QGraphicsWidget):
    @inject.params(gs=GState)
    def __init__(self, gs=None, parent=None):
        logger.info('%s init', self.__class__.__qualname__)
        super().__init__(parent)
        self.sty = gs.sty['Bud']
        self.cfg = gs.cfg
        # self.setStyleSheet("background:transparent")

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
    # def minimalSize(self):
    #     return QSize(10, 10)

    # def sizeHint(self):
    #     return QSize(2*base.R(self), 2*base.R(self))

    # def setGeometry(self, rect):    # rect -- w/o margin
    #     super().setGeometry(rect)   # Necessary for updating masks and own geometry
    #     self.layout().setGeometry(rect)
    #     self.r = self.layout().r
    #     self.dr = self.layout().dr

    #     a = min(self.width(), self.height())
    #     qr = QtCore.QRect(self.width()/2 - a/2, self.height()/2 - a/2, a, a)
    #     rgn = QtGui.QRegion(qr, QtGui.QRegion.Ellipse)
    #     self.setMask(rgn)

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
            p.setPen(QtCore.Qt.NoPen)
            p.setBrush(QtGui.QColor(0, 255, 255, 50))
            p.drawRect(self.geometry())

        def _drawMask(self, p):
            p.setPen(Qt.NoPen)
            p.setBrush(QtGui.QColor(255, 255, 0, 80))
            path = QtGui.QPainterPath()
            path.addRegion(self.mask())
            p.drawPath(path)
