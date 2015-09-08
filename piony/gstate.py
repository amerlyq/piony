from PyQt5.QtCore import QObject, pyqtSignal  # , QRect, QPoint
# from PyQt5.QtWidgets import qApp

from piony import logger
from piony.config import ymlparser as yml
from piony.config.argparser import ArgParser
from piony.config.budparser import BudParser, BudError


class GState(QObject):
    invalidated = pyqtSignal(dict)

    def __init__(self, argv):
        super().__init__()
        logger.info('%s init', self.__class__.__qualname__)
        self.active_window = '%1'
        self.cfg = None
        self.bud = None
        self.now = None  # Instant states like current visibility, etc
        yml.init()
        self._psArg = ArgParser()
        self.update(argv)

    def update(self, argv):
        kgs = self.parse(argv)
        # chg_gs = self.compare(kgs)
        # if chg_gs:
        #     self.invalidated.emit(self.get_gs(), chg_gs)
        logger.info('GState updated')
        self.invalidated.emit(kgs)

    def _set_args_from_command_line(self, cfg, args):
        ar = [(k, v) for k, v in vars(args).items() if v]
        for section, opts in cfg.items():
            for k, v in ar:
                if k in opts:
                    cfg[section][k] = str(v)

    def parse(self, argv):  # NEED: RFC
        args = self._psArg.parse(argv[1:])
        self._psArg.apply(args)  # Set gvars
        cfg = yml.parse(yml.G_CONFIG_PATH)
        self.sty = yml.parse(yml.G_STYLE_PATH)

        if args.kill:
            print("kill:")
            self.quit.emit()

        self._psArg.apply(args)  # Set gvars
        self._set_args_from_command_line(cfg, args)

        entries = args.buds if args.buds else str(cfg['Bud']['default'])
        Bud_Ps = BudParser()
        try:
            bud = Bud_Ps.parse(entries)
        except BudError as e:
            print("Error:", e)
            if not self.bud:  # NOTE: work must go on if client args are bad?
                # qApp.quit()  # don't work until main loop
                raise e

        # TODO: Make 'bReload' as tuple to distinguish necessary refreshes.
        bReload = {}
        bReload['toggle'] = bool(0 == len(argv))
        bReload['Window'] = bool(self.cfg and cfg['Window'] != self.cfg['Window'])

        self.cfg = cfg
        self.bud = bud
        # TODO: ret whole new current state?
        return bReload

    def compare(self, kgs):  # WARNING: broken
        """ Used as separate function because of embedded file paths in arg """
        # Compose dict of current GState variables
        # curr_gs = self.get_gs()
        # Detected changes in global state
        chg_gs = [('cfg', 'Window'), 'bud']
        # TODO: recursive diff cgs/kgs and inserting 1 in changed keys/branches
        return chg_gs

    # TODO: replace with namedtuple (use it to emit)
    def get_gs(self):
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith('__') and not callable(k)}
