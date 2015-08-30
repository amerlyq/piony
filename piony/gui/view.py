from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFrame

from piony.gui import logger, fmt


class MainView(QGraphicsView):
    def __init__(self, wdg, parent=None):
        logger.info('%s: init', self.__class__.__qualname__)
        super().__init__(parent)
        self._setup()
        self._compose(wdg)

    def _compose(self, wdg):
        self._wdg = wdg  # Link to call wdg methods inside scene
        scene = QGraphicsScene()
        scene.addItem(self._wdg)
        self.setScene(scene)
        # self.viewport().installEventFilter(self)
        # self.resize(400, 400)
        # self.resize(scene.width(), scene.height())

    def _setup(self):
        self.setStyleSheet("background:transparent")
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform |
                            QPainter.HighQualityAntialiasing)
        self.setFocusPolicy(Qt.StrongFocus)  # NoFocus
        self.setFrameShape(QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setTransformationAnchor(QGraphicsView.NoAnchor)
        # self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setCacheMode(QGraphicsView.CacheBackground)
        # self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        # self.setSceneRect(QtCore.QRectF(-1e10, -1e10, 2e10, 2e10))

    # def eventFilter(self, obj, e) -> bool:
    #     if e.type() == QEvent.Resize:
    #         logger.info('%s: event %s', self.__class__.__qualname__, str(e.type()))
    #         sz = e.size()
    #         # self._wdg.updateGeometry()
    #         self._wdg.setGeometry(QRectF(0, 0, sz.width(), sz.height()))
    #         return True
    #     return False

    def resizeEvent(self, e):
        sz = e.size()
        logger.info('%s: resize %s, %s', self.__class__.__qualname__,
                    fmt(sz), fmt(self.scene().sceneRect()))
        # CHG: fast (no bud recreation) but blur fonts after scaling
        # THINK: may it be useful for wide scene?
        # TODO: remove it when port all to QGraphics..
        # self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
        # NOTE: eliminates possibility for scrollbars and shrinking
        self.setSceneRect(0, 0, sz.width(), sz.height())

        # self._wdg.setGeometry(0, 0, sz.width(), sz.height())
        # rrf = QRectF(80, 80, sz.width(), sz.height())
        # self._wdg.geometryChanged.emit()
        # self._wdg.setGeometry(rrf)
        # self._wdg.geometryChanged.emit()
        # self._wdg.setGeometry(QRectF(0, 0, sz.width(), sz.height()))
        # self.centerOn(0, 0)
        # self._wdg.layout().updateGeometry()
        super().resizeEvent(e)

        # ALT: create with exact size -- for rare resize
        # self.scene.setSceneRect(self.scene.itemsBoundingRect())
        # if self.wdg.budwdg:
        #     self.scene.clear()
        #     self.wdg = MainWidget()
        #     self.wdg.budwdg.setGeometry(
        #         QRect(0, 0, self.view.width(), self.view.height()))
        #     self.scene.addWidget(self.wdg)
