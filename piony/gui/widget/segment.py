import inject
from PyQt5.QtCore import Qt, QRect  # QSizeF, QPoint,
from PyQt5.QtGui import QColor, QFont, QPen  # , QLinearGradient

import piony
from piony.system.action import sendKey
from piony.gui import logger
from piony.gui.widget import base
from piony.gstate import GState
from piony.gui.items import SegmentItem


# class SegmentWidget(SegmentItem):
#     def __init__(self, clr, **kwargs):
#         super().__init__(**kwargs)
#         self.clr = clr
#         self.text = "A"
#         self._path = None
#         # self.setFlags(QGraphicsItem.ItemIsSelectable |
#         #               QGraphicsItem.ItemIsMovable)

#     def paint(self, p, option, wdg):
#         pen = QPen(Qt.black, 3, Qt.SolidLine)
#         if option.state & QStyle.State_Selected:
#             pen.setColor(Qt.yellow)
#         p.setPen(pen)
#         p.setBrush(self.clr)

#         if self._path:
#             p.drawPath(self._path)
#         if self._text_rf:
#             p.drawText(self._text_rf, Qt.AlignCenter, self.text)


class SegmentWidget(SegmentItem):
    gs = inject.attr(GState)
    _fsm_regime = {'default': 'normal', 'normal': 'select',
                   'select': 'press', 'press': 'select'}

    def __init__(self, sgm, **kwargs):
        logger.info('%s init: %s', self.__class__.__qualname__, str(sgm))
        super().__init__(**kwargs)
        self.sty = self.gs.sty['Segment']
        self.sgm = sgm
        self._text_rf = QRect(0, 0, 16, 16)
        self.font = QFont(str(self.sty['Text']['font']), self._text_rf.height())
        self._regime = 'normal'
        self._path = None
        # self.setMouseTracking(True)
        # self.setFlags(QGraphicsItem.ItemIsSelectable |
        #               QGraphicsItem.ItemIsMovable)
        # self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        # self.setEnabled(True)
        # self.setActive(True)

    def shape(self):
        return self._path

    def _clr(self, name):
        return QColor(*list(self.sty[name]['color'][self._regime]))

    def _nextClr(self, rgm=None):
        self._regime = SegmentWidget._fsm_regime[rgm if rgm else self._regime]
        self.update()

    ## --------------
    def hoverEnterEvent(self, e):
        self._nextClr()

    def hoverLeaveEvent(self, e):
        self._nextClr('default')

    def mousePressEvent(self, e):
        # if e.button() == Qt.LeftButton and _hasModCtrl():
        self._nextClr()

    def mouseReleaseEvent(self, e):
        # if e.button() == Qt.LeftButton and not _hasModCtrl():
        self._nextClr()
        if self.sgm.action:
            sendKey(self.sgm.action)

    ## --------------
    def drawBody(self, p):
        p.setBrush(self._clr("Filler"))
        p.setPen(QPen(self._clr("Border"),
                 float(self.sty['Border']['width']), Qt.SolidLine))
        if self._path:
            p.drawPath(self._path)

    def drawText(self, p):
        sz = self._text_rf.size() * float(self.sty['Text']['scale'])
        base.adjustFontSize(p, self.sgm.name, sz)

        p.setPen(self._clr("Text"))
        if __debug__ and piony.G_DEBUG_VISUALS:
            p.drawRect(self._text_rf)
        if self.sgm.name and self._text_rf:
            p.drawText(self._text_rf, Qt.AlignCenter, self.sgm.name)

    def paint(self, p, opt, wdg):
        # if __debug__ and piony.G_DEBUG_VISUALS:
        #     self.drawSegmentRegion(p)
        self.drawBody(p)
        self.drawText(p)

#     if __debug__:
#         def drawSegmentRegion(self, p):  # Gradient brush
#             grd = QLinearGradient(0, 0, self._r, 0)
#             grd.setColorAt(0.0, QColor(0, 0, 0, 40))
#             grd.setColorAt(1.0, QColor(0, 0, 0, 40))
#             p.setBrush(grd)
#             p.setPen(QPen(Qt.NoPen))
#             p.drawRect(QRect(QPoint(2, 2), self.size() - QSizeF(4, 4)))
