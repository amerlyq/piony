#!/usr/bin/env python3
# vim: fileencoding=utf-8

import piony
from piony import gvars


def G_ARGUMENTS_DEFAULT_F(farg):  # @par1 = Method to add arguments into parser
    ## Configuration
    farg('buds', metavar='bud', nargs='*', type=str,
         help="Setup profile layout in json directly on cmdline. "
              "Can be specified several times -- one for each slice. "
              "Or use pathes to files with slices inside.")
    farg('-c', '--config',
         default=gvars.G_CONFIG_PATH,
         help="Config file with default settings.")
    farg('-p', '--print',
         help="Toggle action print/execute to use as frontend only.")

    ## Appearance
    farg('-s', '--size', type=int, default=360,
         help="Sets window size WxH=NxN to derive all rings sizes from it.")
    farg('-F', '--fullscreen', action='store_true',
         help="Overlay fullscreen/local")
    farg('-T', '--no-tooltip', action='store_true',
         # nargs='?', const='', default='y', choices=[''],
         help="Disable pop-up items, for those who is irritated.")

    ## Process
    farg('-V', '--verbose',
         nargs='?', const='l',
         choices=['l', 'v', 'a'],
         help="Verbose (debug): all (default), or visuals / actions.")
    farg('-v', '--version', action='version',
         version="%(prog)s {0}".format(piony.__version__),
         help="Version of program.")
