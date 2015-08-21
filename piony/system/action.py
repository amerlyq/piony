from subprocess import call
from PyQt5.QtWidgets import qApp

from piony.config import gvars


if __debug__ and gvars.G_DEBUG_ACTIONS:

    # xdotool mousemove --sync 960 460 sleep 0.17 mousedown 1 sleep 0.12 mouseup 1
    def sendKey(key):
        print("Keys: " + key)

    def sysClose():
        print("Qt: close()")

else:

    def sendKey(key):
        cmd = ['xdotool', 'key']
        if gvars.G_ACTIVE_WINDOW:
            cmd.extend(['--window', gvars.G_ACTIVE_WINDOW])
        call(cmd + ['--clearmodifiers', key], shell=False)

    def sysClose():
        qApp.quit()
