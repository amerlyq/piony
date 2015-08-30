import inject
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, qApp

import piony
from piony.gstate import GState
from piony.gui import logger
from piony.gui.view import MainView
from piony.gui.scene import MainScene
from piony.gui.widget.bud import BudWidget
from piony.inputprc import InputProcessor


class MainEventsMixin(object):
    def showEvent(self, e):
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
        # DEV: use center of scene (0,0) instead of window center
        fg = self.geometry()
        cp = QCursor.pos()
        # cp = QApplication.desktop().cursor().pos()
        # screen = QApplication.desktop().screenNumber(cp)
        # sg = QApplication.desktop().screenGeometry(screen)
        fg.moveCenter(cp)
        self.move(fg.topLeft())  # self.setGeometry(fg)


class MainWindow(MainControlMixin, MainEventsMixin, QMainWindow):
    def __init__(self):
        logger.info('%s init', self.__class__.__qualname__)
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
        self.scene = MainScene(self.wdg)
        self.view = MainView(self.scene, self.wdg)
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
