import inject
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtWidgets import QGraphicsItem

import piony
from piony.gui import logger
from piony.gstate import GState
from piony.gui.engine.slice import SliceLayoutEngine
from piony.gui.widget import base
from piony.gui.widget.ring import RingWidget


class SliceWidget(QGraphicsItem):
    @inject.params(gs=GState)
    def __init__(self, slicee, r=None, R=None, gs=None, parent=None):
        logger.info('%s init', self.__class__.__qualname__)
        self._engine = SliceLayoutEngine(r=r, R=R, spacing=4)
        super().__init__(parent)
        self.sty = gs.sty['Bud']
        self.cfg = gs.cfg
        self.text = gs.bud['slices'][0].get('name')
        self._text_rf = QRect(0, 0, 16, 16)
        self.font = QFont(str(self.sty['Text']['font']), self._text_rf.height())
        self.build(slicee)

    def build(self, slicee):
        # BUG: engine don't set boundings
        rings = map(lambda rg: RingWidget(rg, parent=self), slicee['rings'])
        self._engine.insert(rings)

    def boundingRect(self):
        R = self._engine.R
        return QRectF(-R, -R, 2*R, 2*R)

    def paint(self, p, option, wdg):
        if __debug__ and piony.G_DEBUG_VISUALS:
            self._drawDbg(p)
        if self.text:
            self.drawText(p)
        # if self._ring:
        #     self._ring.paint(p, option, wdg)
        for item in self._engine.items:
            item.paint(p, option, wdg)

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
