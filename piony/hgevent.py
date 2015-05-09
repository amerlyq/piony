#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtCore, QtGui, QtWidgets

from piony import action


def _hasModCtrl():
    modifiers = QtWidgets.QApplication.keyboardModifiers()
    return modifiers == Qt.ControlModifier


def _hasModShift(e):
    return e.modifiers() == Qt.ShiftModifier


def _hasModAlt(e):
    return e.modifiers() == Qt.AltModifier


class HGEventMixin:
    def __init__(self):
        self.bM3 = False
        self.bFirstMove = False
        self.ppos = QtCore.QPoint()

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

        if _hasModShift(e):
            print("shift")

        if _hasModAlt(e) and e.key() == Qt.Key_I:
            print("alt + I")

        if e.key() == Qt.Key_K:
            print("KKKKKKKK")
            print(Qt.Key_K)

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
            # NOTE: rgn object must be derived only once at initialization.
            rgn = self.frameGeometry() if self.mask().isEmpty() else self.mask()
            if not rgn.contains(QtGui.QCursor.pos()):
                action.sysClose()

        ## Move window in specified position again, to deal with i3wm workspace.
        if e.type() == QEvent.Show:
            self.bFirstMove = True
        if self.bFirstMove and e.type() == QEvent.Move:
            self.centerOnCursor()
            self.bFirstMove = False
            # print(e.type(), self.geometry())

        # if self.layout().indexOf(obj) != -1:
        #     if event.type() == event.MouseButtonPress:
        #         print("Widget click", obj)

        # return super().eventFilter(obj, e)  # default
        return False
        # True -- event will be filtered and not reach the obj, meaning that I
        # decided to handle it myself

    def resizeEvent(self, e):
        self.budwdg.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), e.size()))
