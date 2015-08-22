from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize

import piony
from piony.widget.bud import BudWidget
from piony.hgevent import HGEventMixin


class WindowContent(QtWidgets.QWidget, HGEventMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = None
        self.budwdg = None
        self.setLayout(QtWidgets.QStackedLayout())
        self.installEventFilter(self)
        self.setMouseTracking(True)

    ## --------------
    def reload(self, cfg, bud, bReload):
        if cfg:
            self.cfg = cfg
        if bud or bReload['Window']:
            self.setContent()

            if self.budwdg:
                self.layout().removeWidget(self.budwdg)
                self.budwdg.close()
            self.budwdg = BudWidget(bud, self.cfg)
            self.layout().addWidget(self.budwdg)
            # QObjectCleanupHandler().add(self.layout())
            # setCurrentWidget to display the one you want.

            self.resize(self.sizeHint())
            self.centerOnCursor()
        if bReload['toggle']:
            self.setVisible(not self.isVisible())
        else:
            # NOTE: don't forget to delete, or --hide will not work later
            self.show()

    def setContent(self):
        if self.cfg['Window'].getboolean('no_tooltip'):
            self.setToolTip(None)
        else:
            QtWidgets.QToolTip.setFont(QtGui.QFont('Ubuntu', 12))
            self.setToolTip('Slice No=1 <i>Click at any empty space to close.</i>')

        aQuit = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                                  triggered=QtWidgets.QApplication.instance().quit)
        # aQuit.setShortcutContext(Qt.WidgetShortcut)
        self.addAction(aQuit)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    ## --------------
    def sizeHint(self):
        return self.budwdg.sizeHint() if self.budwdg else QSize()

    def minimumSize(self):
        return self.budwdg.minimalSize() if self.budwdg else QSize()

    def showEvent(self, e):
        self.centerOnCursor()

    def centerOnCursor(self):
        fg = self.geometry()
        cp = QtGui.QCursor.pos()
        # cp = QtGui.QApplication.desktop().cursor().pos()
        # screen = QtGui.QApplication.desktop().screenNumber(cp)
        # sg = QtGui.QApplication.desktop().screenGeometry(screen)
        fg.moveCenter(cp)
        self.move(fg.topLeft())  # self.setGeometry(fg)

    ## --------------
    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)  # p.begin(self)
        self.drawCleanBkgr(p)
        p.end()

    def drawCleanBkgr(self, p):
        p.setPen(Qt.NoPen)
        p.setBrush(QtGui.QColor(0, 0, 0, 0))
        p.drawRect(self.rect())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setParent(None)  # Create TopLevel-Widget

        # if(QX11Info.isCompositingManagerRunning()):
        self.setAttribute(Qt.WA_TranslucentBackground)
        wflags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        # if not __debug__:
        #     wflags |= Qt.X11BypassWindowManagerHint
        self.setWindowFlags(self.windowFlags() | wflags)
        self.setCentralWidget(WindowContent())

        # self.setStyleSheet("background:transparent;")
        # self.setWindowOpacity(0.7)
        self.setWindowTitle("{} {}".format(piony.__appname__,
                                           piony.__version__))
