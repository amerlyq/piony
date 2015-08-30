from PyQt5.QtWidgets import QGraphicsLayout
from PyQt5.QtCore import Qt, QSizeF, QRectF

from piony.gui import logger
from piony.gui.engine.ring import RingLayoutEngine


class RingLayout(QGraphicsLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._engine = RingLayoutEngine()
        # if parent is not None:
        #     self.setMargin(margin)
        # self.r = r
        # self.dr = dr
        # self.setSpacing(spacing)

    def invalidate(self):
        self._engine.invalidate()
        super().invalidate()

    def count(self):
        return len(self._engine)

    def itemAt(self, idx):
        return self._engine[idx]

    def removeAt(self, idx):
        return self._engine.removeAt(idx)

    def sizeHint(self, which: Qt.SizeHint, constrain: QSizeF):
        # NOTE: will be useful only for Bud -- when Slices could shift one of another
        # size = QSize()
        # for item in self._items:
        #     size = size.expandedTo(item.minimumSize())
        # size += QSize(2 * self.margin(), 2 * self.margin())
        # return size
        # return QSizeF(160, 40)
        return QSizeF(self._engine.R, self._engine.R)

    def setGeometry(self, r):
        super().setGeometry(r)
        self._engine.setGeometries(r, lambda m, *r: m.setGeometry(QRectF(*r)))
        logger.info('%s setG %s', self.__class__.__qualname__, str(self._engine.R))

    # <New>
    def addItem(self, item):
        self.insertItem(-1, item)

    def addStretch(self, stretch=1):
        self.insertStretch(stretch)

    def insertItem(self, pos, item):
        super().addChildLayoutItem(item)
        self._engine.insertItem(pos, item)
        self.invalidate()

    def insertStretch(self, pos, stretch=1):
        self._engine.insertStretch(pos, stretch)
        self.invalidate()
