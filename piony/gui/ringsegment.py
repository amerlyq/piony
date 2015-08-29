from math import degrees, asin, sin, radians, sqrt
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect, QRectF

from piony.common.math import ra2xy, arcContains, lrotate


class RingSegment:

    def __init__(self, r, a, dr, da):     # 4 -- 3
        self.a = a                        # )    )
        self.r = r                        # 1 -- 2
        # if da > 360 or da < 0 -- > raise exception
        self.da = da
        self.dr = dr

    def R(self):
        return self.r + self.dr

    def A(self):
        return self.a + self.da

    def arcFixes(self, lw=0):
        # count separate shift to replace angle spacer on line spacer in between
        def afix(r):
            return degrees(asin(float(lw) / r)) if r else 0
        return [afix(self.r), afix(self.r + self.dr)]

    def points_ra(self, lw=0):
        r = self.r
        R = self.R()
        a = self.a
        A = self.A()
        la, La = self.arcFixes(lw)
        return [ra2xy(r+lw, a+la), ra2xy(R-lw, a+La),
                ra2xy(R-lw, A-La), ra2xy(r+lw, A-la)]

    def limitAt(self, nq, pts):     # nq -- Cartesian quarter number [0..3]
        i = (nq + 1) % 4
        j = nq % 2
        R = self.R()
        if nq % 4 > 1:
            R = -R
        return pts[i][j] if not arcContains(self.a, self.da, nq*90) else R

    def bbox_ra(self):  # Cartesian box relative to ring center in (0,0)
        # NOTE: can be optimized -- as we already knew which dots influence which side
        pts = lrotate(self.points_ra(), -int(self.a / 90))
        r = self.limitAt(0, pts)
        t = self.limitAt(1, pts)
        l = self.limitAt(2, pts)
        b = self.limitAt(3, pts)
        pts = lrotate(self.points_ra(), -int((self.a+self.da) / 90))
        r = max(r, self.limitAt(0, pts))
        t = max(t, self.limitAt(1, pts))
        l = min(l, self.limitAt(2, pts))
        b = min(b, self.limitAt(3, pts))
        return [l, t, r-l, t-b]  # not mirrored, for inner use

    def topLeft_ra(self):
        l, t, w, h = self.bbox_ra()
        return [l, t]

    def points_scr(self, lw=1):
        l, t = self.topLeft_ra()
        return [[fx-l, t-fy] for fx, fy in self.points_ra(lw)]

    def arcCenter_scr(self):
        l, t = self.topLeft_ra()
        return [-l, t]

    ## --- Qt ---------

    def geometry(self, x=0, y=0):  # x,y -- current ring center
        x0, y0 = self.points_ra()[0]
        l, t, w, h = self.bbox_ra()            # mirrored for screen coords
        return QRect(round(x+l-x0), round(y-(t-y0)), round(w), round(h))

    def text_bbox_scr(self, lw=0):
        ## Text: get inscribed circle center tr, and size of inscribed square in it
        R = self.R()
        ha = self.da/2
        hr = self.dr/2
        hra = R - R/(1 + sin(radians(ha)))
        tr = min(hr, hra) if ha < 90 else hr
        tr -= lw
        ta = tr / sqrt(2)
        l, t = self.topLeft_ra()
        cx, cy = ra2xy(R-tr, ha+self.a)
        qr = QRect(cx-ta-l, t-cy-ta, 2*ta, 2*ta)
        return qr

    def path(self, lw=3):  # lw -- line width
        r = self.r + lw
        R = self.R() - lw
        cx, cy = self.arcCenter_scr()
        pts = self.points_scr(lw)
        la, La = self.arcFixes(lw)

        p = QtGui.QPainterPath()
        p.moveTo(*pts[0])
        p.lineTo(*pts[1])
        # p.lineTo(*pts[2])
        p.arcTo(QRectF(cx-R, cy-R, 2*R, 2*R), self.a+La, self.da-2*La)
        p.lineTo(*pts[3])
        # p.lineTo(*pts[0])
        p.arcTo(QRectF(cx-r, cy-r, 2*r, 2*r), self.a+self.da-la, -self.da+2*la)
        return p

    def region(self, path=None):
        if not path:
            path = self.path(0)
        pg = path.toFillPolygon(QtGui.QTransform()).toPolygon()
        return QtGui.QRegion(pg, Qt.WindingFill)
