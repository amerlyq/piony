import inject
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QGraphicsItem

import piony
from piony.gui import logger
from piony.gstate import GState
from piony.gui.widget import base
from piony.gui.widget.ring import RingWidget


class SliceWidget(QGraphicsItem):
    @inject.params(gs=GState)
    def __init__(self, items, r=None, R=None, gs=None, parent=None):
        logger.info('%s init', self.__class__.__qualname__)
        super().__init__(parent)
        self.sty = gs.sty['Bud']
        self.cfg = gs.cfg
        self.text = gs.bud['slices'][0].get('name')
        self._text_rf = QRect(0, 0, 16, 16)
        self.font = QFont(str(self.sty['Text']['font']), self._text_rf.height())

        rings = items[0]['segments']
        self._ring = RingWidget(rings, r=r, R=R, parent=self)
        # segments = map(lambda sgm: SegmentWidget(sgm, parent=self), items)
        # self._engine.insert(segments)

    def boundingRect(self):
        return self._ring.boundingRect()

    def paint(self, p, option, wdg):
        if __debug__ and piony.G_DEBUG_VISUALS:
            self._drawDbg(p)
        if self.text:
            self.drawText(p)
        if self._ring:
            self._ring.paint(p, option, wdg)

    def drawText(self, p):
        sz = self._text_rf.size() * float(self.sty['Text']['scale'])
        base.adjustFontSize(p, self.text, sz)
        p.setPen(QColor(*list(self.sty['Text']['color'])))
        if __debug__ and piony.G_DEBUG_VISUALS:
            p.drawRect(self._text_rf)
        if self.text and self._text_rf:
            p.drawText(self._text_rf, Qt.AlignCenter, self.text)

    # <Dbg> --------------------
    if __debug__:
        def _drawDbg(self, p):
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 255, 255, 50))
            p.drawRect(self.boundingRect())
