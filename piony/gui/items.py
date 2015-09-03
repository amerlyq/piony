from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainterPath

from piony.gui import logger, fmt
from piony.gui.shape.segment import SegmentShapeEngine

# THINK: maybe (r,dr) is betters, as you can skip correctness check R>r


class RingItem(QGraphicsItem):
    def __init__(self, r=None, R=None, engine=None, parent=None):
        super().__init__(parent)
        self._engine = engine
        self._r = r
        self._R = R

    def boundingRect(self):
        # NOTE: return fixed size to keep objects look the same
        # logger.info('bboxR=%-5s : %s', self._R, self.__class__.__qualname__)
        # THINK: maybe cache whole rect?
        return QRectF(-self._R, -self._R, 2*self._R, 2*self._R)

    # <New> --------------------
    def setBoundings(self, **kwargs):
        logger.info('%s := %s', self.__class__.__qualname__, fmt(kwargs))
        if 'r' in kwargs:
            self._r = kwargs.get('r')
        if 'R' in kwargs:
            self._R = kwargs.get('R')
        if self._engine:
            self._engine.update(**kwargs)

    def boundings(self):
        # THINK: cache whole boundings() call in external function?
        # logger.info('%s <R> %f', self.__class__.__qualname__, self._R)
        return (self._r, self._R)


# NOTE: all segments has pos=(0,0), being like pile of layers,
#       each having shifted drawing
class SegmentItem(RingItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._gravity = None      # Text dir - In/Out/Bottom/etc -- for rotating screen

    def boundings(self):
        logger.info('%s <R,A> %f', self.__class__.__qualname__, self._A)
        r, R = super().boundings()
        return (r, R, self._a, self._A)

    def setBoundings(self, **kwargs):
        super().setBoundings(**kwargs)
        if 'a' in kwargs:
            self._a = kwargs.get('a')
        if 'A' in kwargs:
            self._A = kwargs.get('A')
        self.updatePath()

    def updatePath(self, margin=2):
        r, R, a, A = self.boundings()
        sgm = SegmentShapeEngine(r, a, R-r, A-a)

        pts = tuple(map(lambda p: (p[0], -p[1]), sgm.points_ra(margin)))
        (r, al), (_, aL), (R, AL), (_, Al) = sgm.points_RA(margin)

        p = QPainterPath()
        p.moveTo(*pts[0])
        p.lineTo(*pts[1])
        # p.lineTo(*pts[2])
        p.arcTo(QRectF(-R, -R, 2*R, 2*R), aL, AL-aL)
        p.lineTo(*pts[3])
        # p.lineTo(*pts[0])
        p.arcTo(QRectF(-r, -r, 2*r, 2*r), Al, -(Al-al))
        self._path = p
        self._text_rf = QRectF(*sgm.text_bbox_SCR())

    # self.setMask(segment.region())
    # def region(self, path=None):
    #     if not path:
    #         path = self.path(0)
    #     pg = path.toFillPolygon(QtGui.QTransform()).toPolygon()
    #     return QtGui.QRegion(pg, Qt.WindingFill)
