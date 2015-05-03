#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5 import QtGui
from PyQt5.QtCore import Qt


def R(self):
    return self.r + self.dr


# always use 'p' in paintEvent and 'self' in setGeometry
def adjustFontSize(self, text, sz):
    family = self.font().family()
    rw = sz.width()
    rh = sz.height()
    self.setFont(QtGui.QFont(family, int(rh)))
    tsz = self.fontMetrics().size(Qt.TextShowMnemonic, text)  # Qt.TextWordWrap
    fntscale = min(rw / tsz.width(), rh / tsz.height())
    if fntscale < 1:
        self.setFont(QtGui.QFont(family, int(rh * fntscale)))
