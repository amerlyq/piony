#!/usr/bin/env python3
# vim: fileencoding=utf-8

from .common import *
from .ringsegment import *

import math
from PyQt5.QtWidgets import QLayout,QWidgetItem
from PyQt5.QtCore import *

## Storage for inscribed layer data
class SectorWrapper(object):
    def __init__(self, item):
        self.item = item
        self.weight = 1

# Rather SectorStrip, or SectorRing
class SectorLayout(QLayout):
    def __init__(self, r, dr, margin=0, spacing=0, parent=None):
        super().__init__(parent)
        if parent is not None:
            self.setMargin(margin)
        self.r = r
        self.dr = dr
        self.setSpacing(spacing)
        self.sectors = []

    def R(self):
        return self.r + self.dr

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item, pos=0):
        self.sectors.insert(pos, SectorWrapper(item))
        # setDirty()
        # QLayout::invalidate();

    def addWidget(self, widget, pos=0):
        # super(SectorLayout, self).addChildWidget(widget)
        self.addChildWidget(widget)
        self.addItem(QWidgetItem(widget), pos)

    def count(self):
        return len(self.sectors)

    def expandingDirections(self):
        # return QtCore.Qt.Horizontal | QtCore.Qt.Vertical
        # return Qt.Orientations(Qt.Orientation(0))
        return False;

    def itemAt(self, index):
        if index >= 0 and index < len(self.sectors):
            return self.sectors[index].item
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.sectors):
            return self.sectors.pop(index)
        return None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        return w

    def setGeometry(self, rect):     # rect -- w/o margin
        super().setGeometry(rect)
        self.doLayout(rect)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        # size = QSize()
        # for item in self.sectors:
        #     size = size.expandedTo(item.minimumSize())
        # size += QSize(2 * self.margin(), 2 * self.margin())
        # return size
        return QSize(self.R(), self.R())

    def doLayout(self, rect):
        c = rect.center()
        # WARNING: case of empty list -- len([]) == 0
        a = float(360) / len(self.sectors)

        for i, wrapper in enumerate(self.sectors):
            item = wrapper.item
            wdg = item.widget()
            sp = self.spacing()  # may be linear or angle

            segment = RingSegment(self.r, a*i, self.dr, a)
            x,y = ra2xy(self.r, a*i)
            wdg.setGeometry(segment.geometry(c.x()+x, c.y()-y))
            wdg.gPath = segment.path()
            wdg.gText = segment.text_bbox_scr()
            wdg.setMask(segment.region())

