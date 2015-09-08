from PyQt5.QtCore import Qt

from piony.config import ymlparser as yml


G_KEYMAP_PATH = ':/cfgs/keymap.yml'


class KeymapParser:

    def __init__(self):
        yml.init()
        self.keymap = {}
        self.kh = []

    def getQtKeyIndexes(self):
        keysqt = {k[4:]: v for k, v in Qt.__dict__.items() if k.startswith('Key_')}
        keysqt.update({k.lower(): v for k, v in keysqt.items()})

        return keysqt

    def extractKeys(self, keys):
        keysqt = self.getQtKeyIndexes()

        uu = keys.split('-')
        modkeys = 0

        if 'C' in uu:
            modkeys |= int(Qt.ControlModifier)
        if 'S' in uu:
            modkeys |= int(Qt.ShiftModifier)
        if 'A' in uu:
            modkeys |= int(Qt.AltModifier)
        allkeys = (modkeys, keysqt[uu[-1]])

        return allkeys

    def getKeys(self, kmp):
        for ik in kmp:
            self.kh.append(ik)
            if isinstance(kmp[ik], list):
                for keys in kmp[ik]:
                    allkeys = self.extractKeys(keys)
                    self.keymap[allkeys] = tuple(self.kh)
            else:
                self.getKeys(kmp[ik])
            del self.kh[-1]

    def convert(self):
        kmp = yml.parse(G_KEYMAP_PATH)
        self.getKeys(kmp)

        for ik in self.keymap:
            print(ik, self.keymap[ik])

        return self.keymap
