from PyQt5.QtGui import QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt

import piony
from piony.gui import logger
# from piony.gui.layout.ring import RingLayout
from piony.gui.engine.ring import RingLayoutEngine
from piony.gui.items import RingItem
from piony.gui.widget.segment import SegmentWidget


class RingWidget(RingItem):
    def __init__(self, items, **kw):
        engine = RingLayoutEngine(r=kw.get('r'), R=kw.get('R'))
        super().__init__(engine=engine, **kw)
        logger.info('%s init', self.__class__.__qualname__)
        segments = map(lambda sgm: SegmentWidget(sgm, parent=self), items)
        self._engine.insert(segments)

    def paint(self, p, option, wdg):  # : QStyleOptionGraphicsItem, QWidget
        if __debug__ and piony.G_DEBUG_VISUALS:
            self._dbgRingShape(p)
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
