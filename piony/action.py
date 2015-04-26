#!/usr/bin/env python3
# vim: fileencoding=utf-8

import os

from piony import common


# xdotool mousemove --sync 960 460 sleep 0.17 mousedown 1 sleep 0.12 mouseup 1
def sendKey(key):
    cmd = "xdotool key " + key
    if common.G_DEBUG_ACTIONS:
        print(cmd)
    else:
        os.system(cmd)
