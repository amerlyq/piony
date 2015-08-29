import inject
from PyQt5.QtGui import QFont

from piony import logger
from piony.gstate import GState
from piony.gui.window import MainWindow


class MainApplication(object):
    # start = pyqtSignal(list)
    # gs = inject.attr(GState)

    def __init__(self):
        self.create()
        # super().__init__()
        # CHG: bad try to introduce quit event before qapp event loop
        # self.start.connect(self.load)
        # self.start.emit(argv)

    @inject.params(gs=GState)
    def create(self, gs):
        logger.info('%s init', self.__class__.__name__)
        self._globalSetup()
        if gs.cfg['System']['use_tray']:
            self.tray = self._createTray()
        self.srv = self._createServer(gs)
        self.wnd = MainWindow()
        gs.invalidated.connect(self.wnd.reloadState)
        self.wnd.reloadState()
        self.wnd.show()

    def _globalSetup(self):
        from PyQt5.QtWidgets import QToolTip
        QToolTip.setFont(QFont('Ubuntu', 12))

    def _createTray(self):
        from PyQt5.QtWidgets import QSystemTrayIcon
        from PyQt5.QtGui import QIcon
        from piony.common import expand_pj
        tray = QSystemTrayIcon()
        tray.setIcon(QIcon(expand_pj(":/res/tray-normal.png")))
        tray.show()
        return tray

    def _createServer(self, gs):
        from piony.system.server import Server
        srv = Server()
        srv.create()
        # srv.quit.connect(qApp.quit)
        srv.dataReceived.connect(gs.update)
        return srv
