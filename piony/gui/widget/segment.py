import inject
from PyQt5.QtCore import Qt, QRect  # QSizeF, QPoint,
from PyQt5.QtGui import QColor, QFont, QPen  # , QLinearGradient

import piony
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

    def _clr(self, name):
        return QColor(*list(self.sty[name]['color'][self.regime]))

    def __init__(self, name="", act=None, **kwargs):
        logger.info('%s init: %s', self.__class__.__qualname__, name)
        super().__init__(**kwargs)
        self.sty = self.gs.sty['Segment']

        self.text = name
        self.doAction = act
        self.regime = 'normal'

        self._path = None
        self._text_rf = QRect(0, 0, 16, 16)
        self.font = QFont('Ubuntu', self._text_rf.height())
        # self.setMouseTracking(True)
        # self.resize(self.sizeHint())
        # self.setMask(QRegion(rct))
        # self.setFlags(QGraphicsItem.ItemIsSelectable |
        #               QGraphicsItem.ItemIsMovable)
        # self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        # self.setEnabled(True)
        # self.setActive(True)

    def shape(self):
        return self._path

    ## --------------
    def hoverEnterEvent(self, e):
        self.regime = SegmentWidget._fsm_regime[self.regime]
        self.update()

    def hoverLeaveEvent(self, e):
        self.regime = SegmentWidget._fsm_regime['default']
        self.update()

    def mousePressEvent(self, e):
        # if e.button() == Qt.LeftButton and _hasModCtrl():
        self.regime = SegmentWidget._fsm_regime[self.regime]
        self.update()

    def mouseReleaseEvent(self, e):
        # if e.button() == Qt.LeftButton and not _hasModCtrl():
        self.regime = SegmentWidget._fsm_regime[self.regime]
        self.update()
        if self.doAction:
            self.doAction()

    ## --------------
    def drawSegment(self, p):
        p.setBrush(self._clr("Filler"))
        p.setPen(QPen(self._clr("Border"),
                 float(self.sty['Border']['width']), Qt.SolidLine))
        if self._path:
            p.drawPath(self._path)

    def drawSegmentText(self, p):
        ## RFC: Move to setGeometry. BUG: 'self' instead 'p' causes circular call
        sz = self._text_rf.size() * float(self.sty['Text']['scale'])
        base.adjustFontSize(p, self.text, sz)

        p.setPen(self._clr("Text"))
        if __debug__ and piony.G_DEBUG_VISUALS:
            p.drawRect(self._text_rf)
        if self._text_rf:
            p.drawText(self._text_rf, Qt.AlignCenter, self.text)

    def paint(self, p, opt, wdg):
        # if __debug__ and piony.G_DEBUG_VISUALS:
        #     self.drawSegmentRegion(p)
        self.drawSegment(p)
        self.drawSegmentText(p)

#     if __debug__:
#         def drawSegmentRegion(self, p):  # Gradient brush
#             grd = QLinearGradient(0, 0, self._r, 0)
#             grd.setColorAt(0.0, QColor(0, 0, 0, 40))
#             grd.setColorAt(1.0, QColor(0, 0, 0, 40))
#             p.setBrush(grd)
#             p.setPen(QPen(Qt.NoPen))
#             p.drawRect(QRect(QPoint(2, 2), self.size() - QSizeF(4, 4)))
