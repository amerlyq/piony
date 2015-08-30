from piony.gui import logger

from piony.common.math import ra2xy
from piony.gui.ringsegment import RingSegment


class RingLayoutEngine(object):
    def __init__(self):
        self.R = 200
        self.items = []
        self.rotation = 0        # Boundary between first and last items
        self.spacing = 0         # Between items
        self.orientation = None  # Order CW/CCW
        self.gravity = None      # Text dir - In/Out/Bottom/etc -- for rotating screen
        self.invalidate()

    def invalidate(self):
        self._len = None

    def insertItem(self, pos, item):
        self.items.insert(pos, item)

    def insertStretch(self, pos, stretch=1):
        # DEV: self.items.setStretch(stretch)
        pass

    def removeAt(self, idx):
        if isinstance(idx, slice):
            slc = self.items[idx]
            del self.items[idx]
            return slc
        else:
            try:
                return self.items.pop(idx)
            except IndexError:
                logger.exception()
                return None

    def __len__(self):
        if not self._len:  # Cache
            self._len = len(self.items)
        return self._len

    def __setitem__(self, idx, item):
        self.items[idx] = item

    def __getitem__(self, idx):
        try:
            return self.items[idx]
        except IndexError:
            # logger.warning('%s: idx is out of range', self.__class__.__qualname__)
            logger.exception()
            return None

    def __delitem__(self, idx):
        del self.items[idx]

    def __del__(self):
        del self.items

    # DEV: propagate one additional parameter 'innerR' on update
    def setGeometries(self, rf, setGeometryF):     # rect -- w/o margin
        logger.info('%s setGeometry %s', self.__class__.__qualname__, str(rf))
        self.R = min(rf.width(), rf.height()) / 2
        # r = 0.3 * R
        # dr = R - r
        for idx, item in enumerate(self.items):
            nw = rf.width() / len(self.items)
            nx = rf.x() + idx * nw
            setGeometryF(item, nx, rf.y(), nw, nw)

    # OLD:
    def doLayout(self, rect):
        a = min(rect.width(), rect.height())
        self.r = (0.3 * a) // 2
        self.dr = (0.7 * a) // 2
        cx = rect.width()/2
        cy = rect.height()/2

        # WARNING: case of empty list -- len([]) == 0
        a = float(360) / max(1, len(self._items))

        for i, wrapper in enumerate(self._items):
            item = wrapper.item
            wdg = item.widget()
            sp = self.spacing()  # may be linear or angle

            segment = RingSegment(self.r, a*i + sp/2., self.dr, a - sp)
            x, y = ra2xy(self.r, a*i)
            wdg.setGeometry(segment.geometry(cx + x, cy - y))
            wdg.gPath = segment.path()
            wdg.gText = segment.text_bbox_scr()
            wdg.setMask(segment.region())
