from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


def R(self):
    return self.r + self.dr


# always use 'p' in paintEvent and 'self' in setGeometry
def adjustFontSize(self, text, sz):
    family = self.font().family()
    rw, rh = sz.width(), sz.height()
    self.setFont(QFont(family, int(rh)))
    tsz = self.fontMetrics().size(Qt.TextShowMnemonic, text)  # Qt.TextWordWrap
    tw, th = tsz.width(), tsz.height()
    if tw and th:
        fntscale = min(rw / tw, rh / th)
        if fntscale < 1:
            self.setFont(QFont(family, int(rh * fntscale)))
