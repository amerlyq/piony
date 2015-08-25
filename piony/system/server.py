from PyQt5.QtWidgets import qApp
from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtCore import QObject, QDataStream, pyqtSignal

from piony.config import gvars
from piony.config.cfgparser import CfgParser
from piony.config.argparser import ArgsParser
from piony.budparser.parser import BudParser
import piony.budparser.exceptions as bux

# if __debug__:
#     import pprint


def search_dst_window():
    from subprocess import check_output, CalledProcessError
    try:
        out = check_output(['xdotool', 'getactivewindow'])
    except CalledProcessError:
        idwnd = None
    else:
        idwnd = out[:-1].decode('ascii')
    return idwnd


def set_args_from_command_line(cfg, args):
    from piony.config import cfgdefaults
    cd = cfgdefaults.G_CONFIG_DEFAULT

    ar = [(k, v) for k, v in vars(args).items() if v]

    for section, opts in cd.items():
        for k, v in ar:
            if k in opts:
                cfg.set(section, k, str(v))


class Server(QObject):
    from configparser import ConfigParser
    dataReceived = pyqtSignal(ConfigParser, dict, dict)
    quit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cfg = None
        self.bud = None
        self.conn = None
        self.server = None

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
        ## Read configuration files
        # cdir = os.path.dirname(os.path.abspath(__file__))
        # Must be setted up on 'show' action. Move from beginning to appropriate.
        gvars.G_ACTIVE_WINDOW = search_dst_window()

        Arg_Ps = ArgsParser()
        Cfg_Ps = CfgParser()

        cfg = Cfg_Ps.read_file()
        args = Arg_Ps.parse(argv)

        if args.kill:
            print("kill:")
            self.quit.emit()

        Arg_Ps.apply(args)
        set_args_from_command_line(cfg, args)

        entries = args.buds if args.buds else cfg['Bud']['default']
        Bud_Ps = BudParser()
        try:
            bud = Bud_Ps.parse(entries)
        except bux.BudError as e:
            print("Error:", e)
            qApp.quit()

        # if __debug__:
        #     pprint.pprint(bud, width=41, compact=True)

        # TODO: Make 'bReload' as tuple to distinguish necessary refreshes.
        bReload = {}
        bReload['toggle'] = bool(0 == len(argv))
        bReload['Window'] = bool(self.cfg and cfg['Window'] != self.cfg['Window'])

        self.cfg = cfg
        self.bud = bud
        self.dataReceived.emit(self.cfg, self.bud, bReload)
