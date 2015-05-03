#!/usr/bin/env python3
# vim: fileencoding=utf-8

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import piony
from piony import gvars
from piony.config import argdefaults


class ArgsParser:
    def __init__(self):
        self.args = None

    def parse(self, line=None):
        ps = ArgumentParser(prog=piony.__appname__,
                            formatter_class=RawDescriptionHelpFormatter,
                            description=piony.__doc__,
                            epilog="Enjoy!!!")

        argdefaults.G_ARGUMENTS_DEFAULT_F(ps)

        # self.args = ps.parse_args()
        # if line and isinstance(line, basestring):
        if line and isinstance(line, str):
            self.args = ps.parse_args(line.split())
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
