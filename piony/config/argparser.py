#!/usr/bin/env python3
# vim: fileencoding=utf-8

import argparse
from argparse import ArgumentParser as Arg_Pars

import piony
from piony import gvars
from piony.config import argdefaults


class ArgsParser:
    def __init__(self):
        self.args = None

    def parse(self, line=None):
        ps = Arg_Pars(prog=piony.__appname__,
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      description=piony.__doc__,
                      epilog="Enjoy!!!")

        argdefaults.G_ARGUMENTS_DEFAULT_F(ps.add_argument)

        # self.args = ps.parse_args()
        # if line and isinstance(line, basestring):
        if line and isinstance(line, str):
            self.args = ps.parse_args(line.split())
        else:
            self.args = ps.parse_args()

        return self.args

    def apply(self, args=None):
        if not args:
            args = self.args

        dbg = {'l': (True, True), 'v': (True, False), 'a': (False, True)}
        if args.verbose:
            gvars.G_DEBUG_VISUALS, gvars.G_DEBUG_ACTIONS = dbg[args.verbose]

