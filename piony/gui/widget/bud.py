from PyQt5.QtGui import QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt

import piony
from piony.gui import logger
# from piony.gui.layout.ring import RingLayout
from piony.gui.engine.ring import RingLayoutEngine
from piony.gui.items import RingItem
from piony.gui.widget.segment import SegmentWidget


class BudWidget(RingItem):
    def __init__(self):
        super().__init__(engine=RingLayoutEngine())  # NEED: QStackedLayout
        logger.info('%s init', self.__class__.__qualname__)

        # for clr in [Qt.red, QColor(0, 0, 0, 40), Qt.green]:  # , Qt.blue, QColor(255, 255, 255, 40)]:
        for nm in ['a', 'b', 'c']:  # , Qt.blue, QColor(255, 255, 255, 40)]:
            item = SegmentWidget(nm, parent=self)
            self._engine.insertItem(len(self._engine), item)
        # WARNING: Don't use items until you call self.setBoundings!
        self.setBoundings(r=50, R=100)

    def paint(self, p, option, wdg):  # : QStyleOptionGraphicsItem, QWidget
        if __debug__ and piony.G_DEBUG_VISUALS:
            self._dbgPaing(p)
            # self._dbgRingShape(p)
        for item in self._engine.items:
            item.paint(p, option, wdg)

    # <Dbg> --------------------
    if __debug__ and piony.G_DEBUG_VISUALS:
        def _dbgRingShape(self, p):
            r, R, = self.boundings()
            opath = QPainterPath()
            opath.setFillRule(Qt.WindingFill)
            opath.addEllipse(-R, -R, 2*R, 2*R)
            ipath = QPainterPath()
            ipath.setFillRule(Qt.WindingFill)
            ipath.addEllipse(-r, -r, 2*r, 2*r)
            p.fillPath(opath.subtracted(ipath), QColor(255, 255, 0, 50))
            p.strokePath(opath.simplified(), QPen(Qt.black, 3))
            p.strokePath(ipath, QPen(Qt.black, 1))

        def _dbgPaing(self, p):
            # Scene bounds must always be sticked to window borders
            p.setPen(QPen(Qt.white, 3, Qt.SolidLine))
            p.drawRect(self.scene().sceneRect())
            # Axes has inverted Y axis, their base always is sticked to window center
            p.setPen(QPen(Qt.red, 5, Qt.SolidLine))
            p.drawLine(0, 0, 100, 0)
            p.setPen(QPen(Qt.green, 5, Qt.SolidLine))
            p.drawLine(0, 0, 0, 100)
            # Main widget borders must include all slices
            p.setPen(QPen(Qt.magenta, 2, Qt.SolidLine))
            # p.setBrush(QColor(255, 255, 0, 50))
            p.drawRect(self.boundingRect())

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
