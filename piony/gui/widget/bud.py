from PyQt5.QtGui import QColor, QPen, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QStyle
from PyQt5.QtCore import Qt, QRectF

import piony
from piony.gui import logger, fmt
# from piony.gui.layout.ring import RingLayout
from piony.gui.engine.ring import RingLayoutEngine
from piony.gui.engine.segment import SegmentShapeEngine
# from piony.common.math import ra2xy

# THINK: maybe (r,dr) is betters, as you can skip correctness check R>r


class RingItem(QGraphicsItem):
    def __init__(self, engine=None, parent=None):
        super().__init__(parent)
        self._engine = engine

    def boundingRect(self):
        # NOTE: return fixed size to keep objects look the same
        # logger.info('bboxR=%-5s : %s', self.R, self.__class__.__qualname__)
        return QRectF(-self._R, -self._R, 2*self._R, 2*self._R)

    # <New> --------------------
    def setBoundings(self, **kwargs):
        if 'r' in kwargs:
            self._r = kwargs.get('r')
        if 'R' in kwargs:
            self._R = kwargs.get('R')
        if self._engine:
            self._engine.update(**kwargs)

    def boundings(self):
        logger.info('%s <R> %f', self.__class__.__qualname__, self._R)
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
        logger.info('%s setB %s', self.__class__.__qualname__, fmt(kwargs))
        if 'a' in kwargs:
            self._a = kwargs.get('a')
        if 'A' in kwargs:
            self._A = kwargs.get('A')
        super().setBoundings(**kwargs)
        self.updatePath()

    def updatePath(self):
        r, R, a, A = self.boundings()
        sgm = SegmentShapeEngine(r, a, R-r, A-a)

        lw = 2
        pts = tuple(map(lambda p: (p[0], -p[1]), sgm.points_ra(lw)))
        (r, al), (_, aL), (R, AL), (_, Al) = sgm.points_RA(lw)

        p = QPainterPath()
        p.moveTo(*pts[0])
        p.lineTo(*pts[1])
        # p.lineTo(*pts[2])
        p.arcTo(QRectF(-R, -R, 2*R, 2*R), aL, AL-aL)
        p.lineTo(*pts[3])
        # p.lineTo(*pts[0])
        p.arcTo(QRectF(-r, -r, 2*r, 2*r), Al, -(Al-al))
        self._path = p

        # self._text_rf = QRectF(*segment.text_bbox_scr())
        # wdg.setMask(segment.region())

    # def region(self, path=None):
    #     if not path:
    #         path = self.path(0)
    #     pg = path.toFillPolygon(QtGui.QTransform()).toPolygon()
    #     return QtGui.QRegion(pg, Qt.WindingFill)


class SegmentWidget(SegmentItem):
    def __init__(self, clr, **kwargs):
        super().__init__(**kwargs)
        self.clr = clr
        self._path = None
        # self.setFlags(QGraphicsItem.ItemIsSelectable |
        #               QGraphicsItem.ItemIsMovable)

    # def makePath(self):
    #     r, R, a, A = self.boundings()
    #     logger.info('%s bbs %s', self.__class__.__qualname__, fmt((self.clr, self.boundings())))
    #     path = QPainterPath()
    #     # path.moveTo(*ra2xy(0, 0))
    #     path.moveTo(*ra2xy(r, -a))
    #     # path.lineTo(*ra2xy(R, -a))
    #     # path.lineTo(*ra2xy(R, -A))
    #     path.arcTo(QRectF(-R, -R, 2*R, 2*R), a, A-a-40)
    #     path.lineTo(*ra2xy(r, -A+40))
    #     # path.lineTo(*ra2xy(r, -a))
    #     path.arcTo(QRectF(-r, -r, 2*r, 2*r), A-40, -(A-a-40))
    #     path.closeSubpath()
    #     return path

    # def setBoundings(self, **kwargs):
    #     super().setBoundings(**kwargs)
    #     # self._path = self.makePath()

    def paint(self, p, option, wdg):
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        if option.state & QStyle.State_Selected:
            pen.setColor(Qt.yellow)
        p.setPen(pen)
        p.setBrush(self.clr)

        if self._path:
            p.drawPath(self._path)


class BudWidget(RingItem):
    def __init__(self):
        super().__init__(engine=RingLayoutEngine())  # NEED: QStackedLayout
        logger.info('%s init', self.__class__.__qualname__)

        for clr in [Qt.red, QColor(0, 0, 0, 40), Qt.green]:  # , Qt.blue, QColor(255, 255, 255, 40)]:
            item = SegmentWidget(clr, parent=self)
            self._engine.insertItem(len(self._engine), item)
        # WARNING: Don't use items until you call self.setBoundings!
        self.setBoundings(r=50, R=100)
        for item in self._engine.items:
            print(str(item.clr))

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
