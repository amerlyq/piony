from PyQt5.QtCore import Qt
from collections import OrderedDict

from piony.config.keyparser import KeymapParser


class TestKeymapParser:

    def test_getKeys(self):
        kk = KeymapParser()

        kmp = OrderedDict([
                ('Slice', OrderedDict([
                    ('next', ['a'])])),
                ('Ring', OrderedDict([
                    ('rotate', ['C-a', 'C-b'])])),
                ('Button', OrderedDict([
                    ('Inbutton', OrderedDict([
                        ('move', ['i', 'o'])])),
                    ('press', ['u', 'f1']),
                    ('choose', ['C-S-c'])])),
                ('find', ['f', 's'])
            ])

        kk.getKeys(kmp)

        func = kk.keymap.get
        assert ('Slice', 'next') == func((0, Qt.Key_A))
        assert ('Ring', 'rotate') == func((int(Qt.ControlModifier), Qt.Key_A))
        assert ('Ring', 'rotate') == func((int(Qt.ControlModifier), Qt.Key_B))
        assert ('Button', 'Inbutton', 'move') == func((0, Qt.Key_I))
        assert ('Button', 'Inbutton', 'move') == func((0, Qt.Key_O))
        assert ('Button', 'press') == func((0, Qt.Key_U))
        assert ('Button', 'press') == func((0, Qt.Key_F1))
        assert ('Button', 'choose') == func((int(Qt.ControlModifier) | int(Qt.ShiftModifier), Qt.Key_C))
        assert None == func((0, Qt.Key_B))
