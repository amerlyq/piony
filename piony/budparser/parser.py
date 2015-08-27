from piony.config import ymlparser
from piony.budparser.ring import RingMaker
from piony.budparser.slice import SliceMaker


# class BudMaker:
#     """ {slices:[..],...} -> {slices:_} """
#
#     sliceMaker = SliceMaker()
#
#     def make(self, bud):
#
#         lst = map(self.sliceMaker.make, bud)
#         return {"slices": list(lst)}


class BudParser:
    ringMaker = RingMaker()
    sliceMaker = SliceMaker()

    def __init__(self):
        self.default()

    def default(self):
        self.bud = {"slices": []}
        return self.bud

    def interpret(self, entry):
        layer = ymlparser.parse(entry)
        self.bud['slices'].append(self.sliceMaker.make(layer))
        # self.parseEntry(layer)

    def parse(self, entries):
        if not isinstance(entries, list):
            entries = [entries]

        for entry in entries:
            self.interpret(entry)
        return self.bud
