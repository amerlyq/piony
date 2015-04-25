#!/usr/bin/env python3
# vim: fileencoding=utf-8

from . import __doc__
from . import __appname__
from . import __version__
import argparse

def cmd_args():
    ps = argparse.ArgumentParser(prog = __appname__
            , formatter_class = argparse.RawDescriptionHelpFormatter
            , description = __doc__
            , epilog = "Enjoy!!!")

    ps.add_argument('-P', '--pop_up'
            , help="Disable pop-up items, for those who is irritated.")
    ps.add_argument('-d', '--demon'
            , help="Start as background demon.")
    ps.add_argument('-f', '--fullscreen'
            , help="Overlay fullscreen/local")

    ps.add_argument('-v', '--verbose'
            , nargs='?', const='l'
            , choices=['l', 'v', 'a']
            , help="Verbose (debug) {all/{visuals/actions}}.")

    ps.add_argument('-p', '--print'
            , help="Toggle action print/execute.")
    ps.add_argument('-c', '--confpath'
            , help="Path to configs.")
    ps.add_argument('-e', '--setup'
            , help="Setup layout directly on cmdline.")
    ps.add_argument('-s', '--size'
            , type=int, default=360
            , help="Sets window size WxH=NxN to derive all rings sizes from it.")
    ps.add_argument('--version', action='version'
            , version="%(prog)s {0}".format(__version__)
            , help="Version of program.")

#========================================
    # ps.add_argument('-c','--config'
    #         , help="Menu config file with buttons layout. Default in the dir."
    #         , default='config'
    #         )  #required=True)
    # ps.add_argument('-s','--show'
    #         , help="Show menu at current cursor position, or at 'x,y' coords"
    #         , default='auto')
    # ps.add_argument('-H','--hide'
    #         , help="Hide and if has argument '1' click last hovered before it."
    #         , default='auto')
    # ps.add_argument('-D','--no_daemon'
    #         , help="Lauch in normal one-pass mode."
    #         , action='store_true')
    # ps.add_argument('-k','--kill'
    #         , help="Kill demon."
    #         , action='store_true')
    return ps.parse_args()


if __name__ == '__main__':
    pass
