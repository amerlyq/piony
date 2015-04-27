#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtCore, QtGui, QtWidgets

from piony import action


def _hasModCtrl():
    modifiers = QtWidgets.QApplication.keyboardModifiers()
    return modifiers == Qt.ControlModifier


class HGEvent():
    def _dragStart(self, e):
        self.ppos = e.pos()
        self.bM3 = True
        e.accept()

    def keyPressEvent(self, e):
        # Tab, Space -- out of questions as used to choose/press UI elements
        k_ex = [Qt.Key_Escape, Qt.Key_Return]
        if e.key() in k_ex:
            self.close()
            e.accept()

    def mousePressEvent(self, e):
        if e.button() == Qt.MidButton:
            self._dragStart(e)
        elif e.button() == Qt.LeftButton and _hasModCtrl():
            self._dragStart(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and not _hasModCtrl():
            action.sysClose()
        self.bM3 = False  # must drop flag on any mouse button
        # elif e.button() == Qt.MidButton:
        #     e.accept()
        # search "Mozilla Firefox" windowactivate --sync

    def mouseMoveEvent(self, e):
        if self.bM3:
            cp = e.globalPos() - self.ppos
            self.move(cp)

    def wheelEvent(self, e):
        print(e.delta())

    def eventFilter(self, obj, e):
        e_ex = [QEvent.WindowDeactivate, QEvent.Leave]
        if e.type() in e_ex:
            if not self.mask().contains(QtGui.QCursor.pos()):
                action.sysClose()

        # if self.layout().indexOf(obj) != -1:
        #     if event.type() == event.MouseButtonPress:
        #         print("Widget click", obj)

        # return super().eventFilter(obj, e)  # default
        return False
        # True -- event will be filtered and not reach the obj, meaning that I
        # decided to handle it myself

    def resizeEvent(self, e):
        side = min(self.width(), self.height())
        qr = QtCore.QRect(self.width()/2 - side/2, self.height()/2 - side/2, side, side)
        rgn = QtGui.QRegion(qr, QtGui.QRegion.Ellipse)
        self.setMask(rgn)
        self.updateGeometry()
