from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5 import QtGui

from piony.system import action


class InputProcessor(object):
    def __init__(self):
        self._bFirstMove = False
        self._ppos = {'M3': QPoint()}  # last press pos
        self._keys = {'M3': False}
        self._mods = {}

    @staticmethod
    def parse(expr):
        # TODO:
        return expr, 0

    # @property
    # def bM3(self):
    #     return self.__bM3

    # @bM3.setter
    # def bM3(self, b):
    #     self.__bM3 = bool(b)

    def key(self, expr):
        key, mods = InputProcessor.parse(expr)
        return self._keys.get(key, False)

    def delta(self, e, expr):
        key, mods = InputProcessor.parse(expr)
        return e.globalPos() - self._ppos.get(key, QPoint())

    def mPress(self, e):
        # modifiers = QtWidgets.QApplication.keyboardModifiers()
        mkey = 'M' + str(e.button())
        # e.modifiers() == Qt.ControlModifier)
        self._keys[mkey] = True
        self._ppos[mkey] = e.pos()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and not e.modifiers() == Qt.ControlModifier:
            action.sysClose()
        self._bM3 = False  # must drop flag on any mouse button

    def eventFilter(self, obj, e):
        e_ex = [QEvent.WindowDeactivate, QEvent.Leave]
        if e.type() in e_ex:
            # NOTE: rgn object must be derived only once at initialization.
            rgn = self.frameGeometry() if self.mask().isEmpty() else self.mask()
            if not rgn.contains(QtGui.QCursor.pos()):
                action.sysClose()

        ## Move window in specified position again, to deal with i3wm workspace.
        if e.type() == QEvent.Show:
            self._bFirstMove = True
        if self._bFirstMove and e.type() == QEvent.Move:
            self.centerOnCursor()
            self._bFirstMove = False
            # print(e.type(), self.geometry())

        # if self.layout().indexOf(obj) != -1:
        #     if event.type() == event.MouseButtonPress:
        #         print("Widget click", obj)

        # return super().eventFilter(obj, e)  # default
        return False
        # True -- event will be filtered and not reach the obj, meaning that I
        # decided to handle it myself
