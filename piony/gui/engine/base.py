import abc

from piony.gui import logger, fmt


class BaseLayoutEngine(object, metaclass=abc.ABCMeta):
    def __init__(self, **kw):
        self.items = []
        self._len = len(self)
        self.setup(self.defaults(kw))

    @abc.abstractmethod
    def applyToItems(self): pass

    def defaults(self, kw=None):
        members = {'r': None, 'R': None,
                   'rotation': 0, 'spacing': 0, 'inversed': False}
        if kw is not None:
            members.update(kw)
        return members

    def setup(self, kw):
        # THINK: if (filter(kw by dflts) == filter(dflts by kw.keys())):
        # if all([len(self) == self._len, r == self.r, R == self.R]):
        #     return False
        self.__dict__.update({k: kw[k] for k in self.defaults() if k in kw})
        if self.r is None or self.R is None:
            return False
        self._len = len(self)
        return True

    def insertStretch(self, idx, stretch=1):
        # DEV: self.items.setStretch(stretch)
        pass

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

    def update(self, **kw):
        logger.info('%s update %s', self.__class__.__qualname__, fmt(kw))
        if not self.setup(kw) or not self.items:
            return
        self.applyToItems()
