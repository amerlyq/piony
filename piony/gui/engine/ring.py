from piony.gui import logger, fmt


class RingLayoutEngine(object):
    def __init__(self):
        self.items = []
        self.rotation = 0        # Boundary between first and last items
        self.spacing = 0         # Between items, may be linear or angle
        self.orientation = None  # Order CW/CCW
        self.invalidate()

    def invalidate(self):
        self._r = None
        self._R = None

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
        return len(self.items)

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

    def _cacheUpdated(self, r=None, R=None):
        # NOTE: <caching optimization>
        if r == self._r and R == self._R:
            return False
        if r is not None:
            self._r = r
        if R is not None:
            self._R = R
        if self._r is None or self._R is None:
            return False
        return True

    def update(self, **kwargs):
        # WARNING: on first update you must set both 'r' and 'R'
        #       Then self.update() will simply cause re-layouting
        logger.info('%s update %s', self.__class__.__qualname__, fmt(kwargs))
        if not self._cacheUpdated(**kwargs):
            return
        if self.items:
            da = float(360) / len(self.items)
            for i, item in enumerate(self.items):
                item.setBoundings(a=i*da, A=i*da+da, **kwargs)
