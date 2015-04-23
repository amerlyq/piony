#!/usr/bin/env python3
# vim: fileencoding=utf-8

from . import __doc__
import argparse

def cmd_args():
    ps = argparse.ArgumentParser(description=__doc__)
    ps.add_argument('-c','--config'
            , help="Menu config file with buttons layout. Default in the dir."
            , default='config'
            )  #required=True)
    ps.add_argument('-s','--show'
            , help="Show menu at current cursor position, or at 'x,y' coords"
            , default='auto')
    ps.add_argument('-H','--hide'
            , help="Hide and if has argument '1' click last hovered before it."
            , default='auto')
    ps.add_argument('-D','--no-daemon'
            , help="Lauch in normal one-pass mode."
            , action='store_true')
    ps.add_argument('-k','--kill'
            , help="Kill demon."
            , action='store_true')
    return ps.parse_args()


if __name__ == '__main__':
    pass
