from subprocess import call, check_output, CalledProcessError

from PyQt5.QtWidgets import qApp

import piony
from piony import logger


# xdotool mousemove --sync 960 460 sleep 0.17 mousedown 1 sleep 0.12 mouseup 1
def sendKey(key):
    logger.info("Keys: " + key)
    if not __debug__:
        cmd = ['xdotool', 'key']
        if piony.G_ACTIVE_WINDOW:
            cmd.extend(['--window', piony.G_ACTIVE_WINDOW])
        call(cmd + ['--clearmodifiers', key], shell=False)


def sysClose():
    logger.info("Qt: close()")
    if not __debug__:
        qApp.quit()


def search_dst_window():
    try:
        out = check_output(['xdotool', 'getactivewindow'])
    except CalledProcessError:
        idwnd = None
    else:
        idwnd = out[:-1].decode('ascii')
    piony.G_ACTIVE_WINDOW = idwnd
    logger.info("Window -- %s", str(idwnd))
    return idwnd
