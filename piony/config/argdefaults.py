#!/usr/bin/env python3
# vim: fileencoding=utf-8

import piony
from piony import gvars
# from piony.config import cfgdefaults
# import piony.config.cfgdefaults.G_CONFIG_DEFAULT as cfgdef
from piony.config.cfgdefaults import G_CONFIG_DEFAULT as cfgdef


def G_ARGUMENTS_DEFAULT_F(ps):  # @par1 = Method to add arguments into parser
    ## Configuration
    farg=ps.add_argument
    farg('buds', metavar='bud', nargs='*', type=str,
         default=None,
         help="Setup profile layout in json directly on cmdline. "
              "Can be specified several times -- one for each slice. "
              "Or use pathes to files with slices inside.")

    gr_window = ps.add_argument_group('Window')
    gr_window.add_argument('-c', '--config',
         default=None,
         help="Config file with default settings.")
    gr_window.add_argument('-p', '--print',
         default=None,
         help="Toggle action print/execute to use as frontend only.")

    ## Appearance
    gr_window.add_argument('-s', '--size', type=int,
         default=None,
         help="Sets window size WxH=NxN to derive all rings sizes from it.")
    gr_window.add_argument('-F', '--fullscreen', action='store_true',
         default=None,
         help="Overlay fullscreen/local")
    gr_window.add_argument('-T', '--no-tooltip', action='store_true',
         default=None,
         help="Disable pop-up items, for those who is irritated.")

    ## Process
    gr_general = ps.add_argument_group('General')
    gr_general.add_argument('-V', '--verbose',
         nargs='?', const='l',
         choices=['l', 'v', 'a'],
         default=None,
         help="Verbose (debug): all (default), or visuals / actions.")

    farg('-v', '--version', action='version',
         default=None,
         version="%(prog)s {0}".format(piony.__version__),
         help="Version of program.")
