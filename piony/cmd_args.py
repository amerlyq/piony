#!/usr/bin/env python3
# vim: fileencoding=utf-8

import argparse

T_DESC="""
    Wacom Overlay Layer :: radial menu graph for wacom devices
"""

## SEE:
#    https://docs.python.org/3/library/argparse.html
#    https://pythonhosted.org/kitchen/unicode-frustrations.html
#    https://docs.python.org/2/tutorial/introduction.html#tut-unicodestrings

def cmd_args():
    ps = argparse.ArgumentParser(description=T_DESC)
    ps.add_argument('-c','--config'
            , help="Menu config file with buttons layout. Default in the dir."
            , default='config'
            )  #required=True)
    ps.add_argument('-s','--show'
            , help="Show menu at current cursor position, or at 'x,y' coords"
            , default='auto')
    ps.add_argument('-h','--hide'
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
