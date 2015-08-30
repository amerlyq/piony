from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsItem, QStyle
from PyQt5.QtCore import Qt, QRectF

import piony
from piony.gui import logger, fmt
# from piony.gui.layout.ring import RingLayout
from piony.gui.engine.ring import RingLayoutEngine


class RadialItem(QGraphicsItem):
    def __init__(self, engine=None):
        super().__init__()
        self.engine = engine
        self.x = 0
        self.y = 0

    @property
    def R(self):
        return self.engine.R if self.engine else 0

    @R.setter
    def R(self, R):
        logger.info('%s <R> %f', self.__class__.__qualname__, R)
        if self.engine:
            self.engine.R = R
            self.engine.update()
        # self.engine.update()


class MyItem(RadialItem):
    def __init__(self, R, clr):
        super().__init__()
        self.R = R
        self.clr = clr
        # self.setPos(0, 0)
        # self.setFlags(QGraphicsItem.ItemIsSelectable |
        #               QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        # NOTE: return fixed size to keep objects look the same
        return QRectF(self.x, self.y, self.R, self.R)

    def paint(self, p, option, wdg):
        pen = QtGui.QPen(Qt.black, 3, Qt.SolidLine)
        if option.state & QStyle.State_Selected:
            pen.setColor(Qt.yellow)
        p.setPen(pen)
        p.setBrush(self.clr)
        r = self.boundingRect()
        p.drawEllipse(r)  # option.rect


class BudWidget(RadialItem):
    def __init__(self):
        super().__init__(RingLayoutEngine())  # NEED: QStackedLayout
        logger.info('%s init', self.__class__.__qualname__)

        for clr in [Qt.red, Qt.green, Qt.blue, QtGui.QColor(255, 255, 255, 40)]:
            item = MyItem(40, clr)
            logger.info('%s', fmt(item.boundingRect()))
            self.engine.insertItem(-1, item)

    def boundingRect(self):
        logger.info('%s bbox %s', self.__class__.__qualname__, fmt(self.engine.R))
        return QRectF(0, 0, self.R, self.R)

    # def setGeometry(self, r):
    #     super().setGeometry(r)
    #     # self.layout().setGeometry(r)
    #     logger.info('%s setGeometry %s', self.__class__.__qualname__, fmt(self.geometry()))

    def paint(self, p, option, wdg):  # : QStyleOptionGraphicsItem, QWidget
        if __debug__ and piony.G_DEBUG_VISUALS:
            p.setPen(QtGui.QPen(Qt.magenta, 3, Qt.SolidLine))
            p.drawRect(self.boundingRect())
            p.setPen(QtGui.QPen(Qt.red, 5, Qt.SolidLine))
            p.drawLine(0, 0, 100, 0)
            p.setPen(QtGui.QPen(Qt.green, 5, Qt.SolidLine))
            p.drawLine(0, 0, 0, 100)
        for item in self.engine.items:
            item.paint(p, option, wdg)

    # <New> --------------------
    def refreshBuds(self):
        logger.info('%s: buds', self.__class__.__qualname__)
        # if self.wdg:
        #     self.layout().removeWidget(self.wdg)
        #     self.wdg.close()
        # self.wdg = SliceWidget()
        # self.layout().addItem(self.wdg)
        # QObjectCleanupHandler().add(self.layout())
        # self.setCurrentWidget(wdg) to display the one you want.
        # self.resize(self.sizeHint())
