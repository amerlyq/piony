import inject
from PyQt5.QtCore import Qt  # , QRect, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QMainWindow, QGraphicsView, QGraphicsScene, qApp)

import piony
from piony.widget.bud import BudWidget
from piony.inputprc import InputProcessor
from piony.gstate import GState


class MainView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self._setup()
        self.setScene(scene)
        self.resize(scene.width(), scene.height())

    def _setup(self):
        self.setStyleSheet("background:transparent")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCacheMode(QGraphicsView.CacheBackground)


class MainEventsMixin(object):
    def showEvent(self, e):
        self.adjustSize()
        self.centerOnCursor()

    def keyPressEvent(self, e):
        # Tab, Space -- out of questions as used by Qt (and me in future)
        #   to choose/press UI elements
        if e.key() in [Qt.Key_Escape, Qt.Key_Return]:
            qApp.quit()
        if e.modifiers() == Qt.ShiftModifier and e.key() == Qt.Key_K:
            print("K")
            e.accept()

    def mousePressEvent(self, e):
        # print(e.button())
        self.ipr.mPress(e)
        # e.accept()

    def mouseMoveEvent(self, e):
        if self.key('M3') or self.key('C-M1'):
            self.move(self.ipr.delta(e, 'M3'))

    def resizeEvent(self, e):
        self.adjustSize()

    def wheelEvent(self, e):
        print("Ring rotate: ", e.angleDelta())


class MainControlMixin(object):
    def setupDynamic(self, cfg):
        wflags = self.windowFlags()
        if bool(cfg['System']['no_focus']):
            wflags |= Qt.X11BypassWindowManagerHint
        else:
            wflags &= ~Qt.X11BypassWindowManagerHint
        self.setWindowFlags(wflags)

        if not bool(cfg['Window']['no_tooltip']):
            text = 'Slice No=1 <i>Click at any empty space to close.</i>'
        self.setToolTip(text if text else None)

    def centerOnCursor(self):
        fg = self.geometry()
        cp = QCursor.pos()
        # cp = QApplication.desktop().cursor().pos()
        # screen = QApplication.desktop().screenNumber(cp)
        # sg = QApplication.desktop().screenGeometry(screen)
        fg.moveCenter(cp)
        self.move(fg.topLeft())  # self.setGeometry(fg)

    def adjustSize(self):
        # CHG: fast (no bud recreation) but blur fonts after scaling
        # THINK: may it be useful for wide scene?
        # TODO: remove it when port all to QGraphics..
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        # ALT: create with exact size -- for rare resize
        # self.scene.setSceneRect(self.scene.itemsBoundingRect())
        # if self.wdg.budwdg:
        #     self.scene.clear()
        #     self.wdg = MainWidget()
        #     self.wdg.budwdg.setGeometry(
        #         QRect(0, 0, self.view.width(), self.view.height()))
        #     self.scene.addWidget(self.wdg)


class MainWindow(MainControlMixin, MainEventsMixin, QMainWindow):
    def __init__(self):
        super().__init__()
        self._setupWindow()
        self._attachElements()
        self._setupContextMenu()

    @inject.params(gs=GState)
    def reloadState(self, chgs={}, gs=None):
        if gs.cfg:
            self.setupDynamic(gs.cfg)
        if gs.bud or gs.bReload['Window']:
            # self.scene.clear()
            # self.wdg = BudWidget(gs.bud, gs.cfg)
            # self.scene.addWidget(self.wdg)
            self.wdg.refreshBuds()
            self.centerOnCursor()
        if chgs.get('toggle', False):
            self.setVisible(not self.isVisible())

    def _attachElements(self):
        self.ipr = InputProcessor()
        self.wdg = BudWidget()
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.wdg)
        self.view = MainView(self.scene)
        self.setCentralWidget(self.view)

    def _setupWindow(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        wflags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        self.setWindowFlags(self.windowFlags() | wflags)
        self.installEventFilter(self)
        self.setMouseTracking(True)

        self.setMinimumSize(10, 10)
        self.setWindowTitle("{} {}".format(
            piony.__appname__, piony.__version__))

    def _setupContextMenu(self):
        from PyQt5.QtWidgets import QAction
        # SEE: http://doc.qt.io/qt-5/qtwidgets-mainwindows-menus-example.html
        aQuit = QAction("E&xit", self, shortcut="Ctrl+Q",
                        shortcutContext=Qt.ApplicationShortcut,
                        triggered=qApp.quit)
        self.addAction(aQuit)
        # TODO: for release use Qt.NoContextMenu, enable only in edit-mode
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
