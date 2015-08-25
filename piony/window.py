from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import (
    QMainWindow, QGraphicsView, QGraphicsScene,
    QAction, QToolTip, QWidget, QStackedLayout, qApp
)

import piony
from piony.widget.bud import BudWidget
from piony.hgevent import HGEventMixin


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
            qApp.quit()
        if e.modifiers() == Qt.ShiftModifier and e.key() == Qt.Key_K:
            print("K")
            e.accept()


class MainControlMixin(object):
    def setupDynamic(self, cfg):
        wflags = self.windowFlags()
        if cfg['System'].getboolean('no_focus'):
            wflags |= Qt.X11BypassWindowManagerHint
        else:
            wflags &= ~Qt.X11BypassWindowManagerHint
        self.setWindowFlags(wflags)

        if not cfg['Window'].getboolean('no_tooltip'):
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


class MainWindow(MainControlMixin, MainEventsMixin, QMainWindow):
    def __init__(self):
        super().__init__()
        self._setupWindow()
        self._attachElements()
        self._setupContextMenu()

    def _attachElements(self):
        self.wdg = MainWidget()
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.wdg)
        self.view = MainView(self.scene)
        self.setCentralWidget(self.view)

    def _setupWindow(self):
        QToolTip.setFont(QFont('Ubuntu', 12))

        self.setAttribute(Qt.WA_TranslucentBackground)
        wflags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        self.setWindowFlags(self.windowFlags() | wflags)

        self.setMinimumSize(10, 10)
        self.setWindowTitle("{} {}".format(
            piony.__appname__, piony.__version__))

    def _setupContextMenu(self):
        # SEE: http://doc.qt.io/qt-5/qtwidgets-mainwindows-menus-example.html
        aQuit = QAction("E&xit", self, shortcut="Ctrl+Q",
                        shortcutContext=Qt.ApplicationShortcut,
                        triggered=qApp.quit)
        self.addAction(aQuit)
        # TODO: for release use Qt.NoContextMenu, enable only in edit-mode
        self.setContextMenuPolicy(Qt.ActionsContextMenu)


class MainApplication(QObject):
    start = pyqtSignal(list)

    def __init__(self, argv):
        super().__init__()
        from os import path as fs
        self.dir_res = fs.join(fs.dirname(fs.abspath(argv[0])), 'res', '')
        self.start.connect(self.load)
        self.start.emit(argv)

    def load(self, argv):
        self.tray = self._createTray()
        self.srv = self._createServer()
        self.wnd = MainWindow()
        self.srv.loadData(argv[1:])
        self.wnd.show()

    def reloadState(self, cfg, bud, bReload):
        if cfg:
            self.wnd.setupDynamic(cfg)
            self.cfg = cfg
        if bud or bReload['Window']:
            self.wnd.wdg.refreshBuds(cfg, bud)
            self.wnd.centerOnCursor()
        if bReload['toggle']:
            self.wnd.setVisible(not self.wnd.isVisible())

    def _createTray(self):
        from PyQt5.QtWidgets import QSystemTrayIcon
        from PyQt5.QtGui import QIcon
        tray = QSystemTrayIcon()
        tray.setIcon(QIcon(self.dir_res + "tray-normal.png"))
        tray.show()
        return tray

    def _createServer(self):
        from piony.system.server import Server
        srv = Server()
        srv.create()
        # srv.quit.connect(qApp.quit)
        srv.dataReceived.connect(self.reloadState)
        return srv
