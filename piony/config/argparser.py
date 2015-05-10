#!/usr/bin/env python3
# vim: fileencoding=utf-8

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from piony import __appname__, __doc__
from piony.config import gvars
from piony.config import argdefaults


class ArgsParser:
    def __init__(self):
        self.args = None

    def parse(self, cmdline=None):
        ps = ArgumentParser(prog=__appname__,
                            formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__,
                            epilog="Enjoy!!!")

        argdefaults.G_ARGUMENTS_DEFAULT_F(ps)

        if cmdline and isinstance(cmdline, str):
            self.args = ps.parse_args(cmdline.split())
        else:
            self.args = ps.parse_args()

        return self.args

    def apply(self, args=None):
        from operator import xor
        if not args:
            args = self.args
        res = (False, False)
        dbg = {'a': (True, True), 'v': (True, False), 'k': (False, True)}
        if args.verbose:
            for entry in args.verbose:
                res = map(xor, res, dbg[entry])
            gvars.G_DEBUG_VISUALS, gvars.G_DEBUG_ACTIONS = res
