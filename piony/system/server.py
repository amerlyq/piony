from PyQt5.QtWidgets import qApp
from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtCore import QObject, QDataStream, pyqtSignal

import piony.config.processor as prc
import piony.budparser.exceptions as bux
from piony.config import gvars
from piony.config.argparser import ArgsParser
from piony.budparser.parser import BudParser
from piony.system import action

# if __debug__:
#     import pprint
#     pprint.pprint(bud, width=41, compact=True)


def set_args_from_command_line(cfg, args):
    ar = [(k, v) for k, v in vars(args).items() if v]
    for section, opts in cfg.items():
        for k, v in ar:
            if k in opts:
                cfg[section][k] = str(v)


class Server(QObject):
    from collections import OrderedDict
    dataReceived = pyqtSignal(OrderedDict, dict, dict)
    quit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cfg = None
        self.bud = None
        self.conn = None
        self.server = None
        prc.init()

    def create(self, name=gvars.G_SOCKET_NAME):
        QLocalServer.removeServer(name)
        self.server = QLocalServer()
        if not self.server.listen(name):
            print("Error: server -- unable to start: {}."
                  .format(self.server.errorString()))
            self.quit.emit()
        self.server.newConnection.connect(self.notify)

    def close(self):
        self.server.close()

    def notify(self):
        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server: 1 new conn")
        # WARNING: when multiple connections, each will overwrite previous!
        self.conn = self.server.nextPendingConnection()
        self.conn.readyRead.connect(self.receiveData)
        self.conn.disconnected.connect(self.conn.deleteLater)

    def receiveData(self):
        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server: waits for data")

        ins = QDataStream(self.conn)
        ins.setVersion(QDataStream.Qt_5_0)
        if ins.atEnd():
            return
        argv = ins.readQVariant()

        if __debug__ and gvars.G_DEBUG_SERVER:
            print("Server reads:", argv)

        self.loadData(argv)

    def loadData(self, argv):
        # Must be setted up on 'show' action. Move from beginning to appropriate.
        action.search_dst_window()

        Arg_Ps = ArgsParser()

        cfg = prc.load(prc.G_CONFIG_PATH)
        args = Arg_Ps.parse(argv)

        if args.kill:
            print("kill:")
            self.quit.emit()

        Arg_Ps.apply(args)
        set_args_from_command_line(cfg, args)

        entries = args.buds if args.buds else str(cfg['Bud']['default'])
        Bud_Ps = BudParser()
        try:
            bud = Bud_Ps.parse(entries)
        except bux.BudError as e:
            print("Error:", e)
            if not self.bud:  # NOTE: work must go on if client args are bad
                qApp.quit()

        # TODO: Make 'bReload' as tuple to distinguish necessary refreshes.
        bReload = {}
        bReload['toggle'] = bool(0 == len(argv))
        bReload['Window'] = bool(self.cfg and cfg['Window'] != self.cfg['Window'])

        self.cfg = cfg
        self.bud = bud
        self.dataReceived.emit(self.cfg, self.bud, bReload)
