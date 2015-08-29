from argparse import ArgumentParser, RawDescriptionHelpFormatter

import piony
from piony.common.exceptions import InputError


class ArgParser(object):
    def __init__(self):
        self.ps = ArgumentParser(prog=piony.__appname__,
                                 formatter_class=RawDescriptionHelpFormatter,
                                 description=piony.__doc__, epilog="Enjoy!!!")
        self._setup_options()

    def parse(self, argv):
        if not argv:
            argv = []
        elif isinstance(argv, str):
            argv = argv.split()
        elif not isinstance(argv, list):
            raise InputError("Wrong argv type: {}".format(type(argv)))
        return self.ps.parse_args(argv)

    def apply(self, args):
        from operator import xor
        res = (False, False)
        dbg = {'a': (True, True), 'v': (True, False), 'k': (False, True)}
        if args.verbose:
            for entry in args.verbose:
                res = map(xor, res, dbg[entry])
            piony.G_DEBUG_VISUALS, piony.G_DEBUG_ACTIONS = res

    def _setup_options(self):
        ## Configuration
        farg = self.ps.add_argument
        farg('buds', metavar='bud', nargs='*', type=str, default=None,
             help="Setup profile layout in json directly on cmdline. "
                  "Can be specified several times -- one for each slice. "
                  "Or use pathes to files with slices inside.")
        farg('-v', '--version', action='version', default=None,
             version="%(prog)s {0}".format(piony.__version__),
             help="Version of program.")

        gr_window = self.ps.add_argument_group('Window')
        warg = gr_window.add_argument
        warg('-c', '--config', default=None,
             help="Config file with default settings.")
        warg('-p', '--print', default=None,
             help="Toggle action print/execute to use as frontend only.")

        ## Appearance
        warg('-s', '--size', type=int, default=None,
             help="Sets window size WxH=NxN to derive all rings sizes from it.")
        warg('-F', '--fullscreen', action='store_true', default=None,
             help="Overlay fullscreen/local")
        warg('-T', '--no-tooltip', action='store_true', default=None,
             help="Disable pop-up items, for those who is irritated.")

        ## Process
        gr_general = self.ps.add_argument_group('General')
        garg = gr_general.add_argument
        garg('-k', '--kill', action='store_true', default=None,
             help="Kill running daemonized program.")
        garg('-V', '--verbose', nargs='?', type=str,
             const='a', choices=['a', 'v', 'k'], default=None,
             help="Verbose (debug): [a]ll (default), [v]isuals, [k]eys.")
