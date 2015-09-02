import inject
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt

import piony
from piony.gstate import GState
from piony.gui import logger
from piony.gui.widget.ring import RingWidget


class BudWidget(QGraphicsItem):
    @inject.params(gs=GState)
    def __init__(self, gs, parent=None):
        super().__init__(parent)  # NEED: QStackedLayout
        logger.info('%s init', self.__class__.__qualname__)

        items = gs.bud['slices'][0]['rings'][0]['segments']
        self._ring = RingWidget(items, r=100, R=200, parent=self)

    # m.prepareGeometryChange()
    # DEV caching
    def boundingRect(self):
        # size = QSizeF()
        # for item in self._items:
        #     size = size.expandedTo(item.minimumSize())
        # size += QSize(2 * self.margin(), 2 * self.margin())
        # return size
        return self._ring.boundingRect()

    def paint(self, p, option, wdg):
        if __debug__ and piony.G_DEBUG_VISUALS:
            self._dbgPaing(p)
        self._ring.paint(p, option, wdg)

    # <Dbg> --------------------
    if __debug__ and piony.G_DEBUG_VISUALS:
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
