#!/usr/bin/env python3
# vim: fileencoding=utf-8

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from piony import __appname__, __doc__
from piony.config import gvars
from piony.exceptions import PionyError
from piony.config import argdefaults


class ArgsError(PionyError):
    pass


class ArgsInputError(ArgsError):
    pass


class ArgsParser:

    def parse(self, cmdline):
        ps = ArgumentParser(prog=__appname__,
                            formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__,
                            epilog="Enjoy!!!")

        argdefaults.G_ARGUMENTS_DEFAULT_F(ps)

        if not cmdline:
            cmdline = []
        elif isinstance(cmdline, str):
            cmdline = cmdline.split()
        elif not isinstance(cmdline, list):
            raise ArgsInputError()

        return ps.parse_args(cmdline)

    def apply(self, args):
        from operator import xor
        res = (False, False)
        dbg = {'a': (True, True), 'v': (True, False), 'k': (False, True)}
        if args.verbose:
            for entry in args.verbose:
                res = map(xor, res, dbg[entry])
            gvars.G_DEBUG_VISUALS, gvars.G_DEBUG_ACTIONS = res
