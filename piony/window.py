from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import (
    QMainWindow, QGraphicsView, QGraphicsScene,
    QAction, QToolTip, QWidget, QStackedLayout, qApp
)

import piony
from piony.widget.bud import BudWidget
from piony.hgevent import HGEventMixin
from piony.config.cfgparser import CfgParser


class MainWidget(QWidget, HGEventMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.budwdg = None
        self.setLayout(QStackedLayout())
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setStyleSheet("background:transparent")

    def refreshBuds(self, cfg, bud):
        if self.budwdg:
            self.layout().removeWidget(self.budwdg)
            self.budwdg.close()
        self.budwdg = BudWidget(bud, cfg)
        self.layout().addWidget(self.budwdg)
        # QObjectCleanupHandler().add(self.layout())
        # self.setCurrentWidget(wdg) to display the one you want.
        self.resize(self.sizeHint())


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
        self.centerOnCursor()

    def keyPressEvent(self, e):
        # Tab, Space -- out of questions as used by Qt (and me in future)
        #   to choose/press UI elements
        if e.key() in [Qt.Key_Escape, Qt.Key_Return]:
            self.close()
        if e.modifiers() == Qt.ShiftModifier and e.key() == Qt.Key_K:
            print("K")
            e.accept()


class MainSettingsMixin(object):
    def attachElements(self):
        self.wdg = MainWidget()
        scene = QGraphicsScene()
        scene.addWidget(self.wdg)
        self.setCentralWidget(MainView(scene))

    def setupWindow(self):
        QToolTip.setFont(QFont('Ubuntu', 12))

        self.setAttribute(Qt.WA_TranslucentBackground)
        wflags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        self.setWindowFlags(self.windowFlags() | wflags)

        self.setMinimumSize(10, 10)
        self.setWindowTitle("{} {}".format(
            piony.__appname__, piony.__version__))

    def setupContextMenu(self):
        # SEE: http://doc.qt.io/qt-5/qtwidgets-mainwindows-menus-example.html
        aQuit = QAction("E&xit", self, shortcut="Ctrl+Q",
                        shortcutContext=Qt.ApplicationShortcut,
                        triggered=qApp.quit)
        self.addAction(aQuit)
        # TODO: for release use Qt.NoContextMenu, enable only in edit-mode
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def setupDynamic(self):
        wflags = self.windowFlags()
        if self.cfg['System'].getboolean('no_focus'):
            wflags |= Qt.X11BypassWindowManagerHint
        else:
            wflags &= ~Qt.X11BypassWindowManagerHint
        self.setWindowFlags(wflags)

        if not self.cfg['Window'].getboolean('no_tooltip'):
            text = 'Slice No=1 <i>Click at any empty space to close.</i>'
        self.setToolTip(text if text else None)


class MainWindow(MainSettingsMixin, MainEventsMixin, QMainWindow):
    def __init__(self):
        super().__init__()
        self.cfg = CfgParser().default()

        self.setupWindow()
        self.setupDynamic()
        self.attachElements()
        self.setupContextMenu()

    def reload(self, cfg, bud, bReload):
        if cfg:
            self.cfg = cfg
            self.setupDynamic()
        if bud or bReload['Window']:
            self.wdg.refreshBuds(cfg, bud)
            self.centerOnCursor()
        if bReload['toggle']:
            self.setVisible(not self.isVisible())
        else:
            # NOTE: don't forget to delete, or --hide will not work later
            self.show()

    def centerOnCursor(self):
        fg = self.geometry()
        cp = QCursor.pos()
        # cp = QApplication.desktop().cursor().pos()
        # screen = QApplication.desktop().screenNumber(cp)
        # sg = QApplication.desktop().screenGeometry(screen)
        fg.moveCenter(cp)
        self.move(fg.topLeft())  # self.setGeometry(fg)
