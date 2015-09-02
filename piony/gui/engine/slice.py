from piony.gui import logger, fmt


class SliceLayoutEngine(object):
    def __init__(self, r=None, R=None):
        self.items = []
        self.rotation = 0        # For all items as whole
        self.spacing = 0         # Between rings
        self.orientation = None  # Order inside/outside
        # Cache
        self._len = len(self)
        self._r = r
        self._R = R

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
        self.update()

    def __del__(self):
        del self.items
        self.update()

    def insert(self, item, idx=None):
        if not idx:
            idx = len(self)
        try:
            self[idx:idx] = item
        except TypeError:
            self[idx:idx] = [item]
        self.update()

    def removeAt(self, idx):
        if isinstance(idx, slice):
            slc = self[idx]
            del self[idx]
            return slc
        else:
            try:
                return self.items.pop(idx)
            except IndexError:
                logger.exception()
                return None

    def _cacheUpdated(self, r=None, R=None):
        # NOTE: <caching optimization>
        if len(self) == self._len:
            return False
        else:
            self._len = len(self)
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
        logger.info('%s update %s', self.__class__.__qualname__, fmt(kwargs))
        if not self._cacheUpdated(**kwargs):
            return
        if self.items:
            dr = float(self._R - self._r) / len(self.items)
            for i, item in enumerate(self.items):
                r = self._r + i*dr
                item.setBoundings(r=r, R=r+dr)
