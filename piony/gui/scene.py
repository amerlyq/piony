from PyQt5.QtWidgets import QGraphicsScene

from piony.gui import logger


class MainScene(QGraphicsScene):
    def __init__(self, wdg, parent=None):
        logger.info('%s: init', self.__class__.__qualname__)
        super().__init__(parent)
        self._wdg = wdg
        self.addItem(wdg)

    # <New>
    def resize(self, sz):
        # self._wdg.resize(sz.width(), sz.height())
        logger.info('%s: resize %s', self.__class__.__qualname__,
                    str(self._wdg.size()))
        # self.setSceneRect(self.itemsBoundingRect())
