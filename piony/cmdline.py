#!/usr/bin/env python3
# vim: fileencoding=utf-8

import argparse

import piony


def cmd_args():
    ps = argparse.ArgumentParser(prog=piony.__appname__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=piony.__doc__,
                                 epilog="Enjoy!!!")
    farg = ps.add_argument

    ## Configuration
    farg('-c', '--config',
         default='cfgs/map.json',
         help="Config file for buttons layout.")
    farg('-e', '--entry',
         help="Setup layout directly on cmdline.")
    farg('-p', '--print',
         help="Toggle action print/execute to use as frontend only.")

    ## Appearance
    farg('-s', '--size',
         type=int, default=360,
         help="Sets window size WxH=NxN to derive all rings sizes from it.")
    farg('-f', '--fullscreen', action='store_true',
         help="Overlay fullscreen/local")
    farg('-T', '--no-tooltip',
         help="Disable pop-up items, for those who is irritated.")

    ## Process
    farg('-V', '--verbose',
         nargs='?', const='l',
         choices=['l', 'v', 'a'],
         help="Verbose (debug): all (default), or visuals / actions.")
    farg('-v', '--version', action='version',
         version="%(prog)s {0}".format(piony.__version__),
         help="Version of program.")

    return ps.parse_args()

