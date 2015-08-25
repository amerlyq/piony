import os
import sys
import yaml

import piony.budparser.exceptions as bux
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
        if not entry:
            layer = None
        elif '-' == entry:
            layer = yaml.safe_load(sys.stdin)  # entry = sys.stdin.read()
        elif os.path.isfile(entry):            # && os.path.isabs(PATH)
            with open(entry, 'r') as f:
                layer = yaml.safe_load(f)      # entry = f.read()
        else:
            layer = yaml.safe_load(entry)

        if layer and not isinstance(layer, (list, dict)):
            raise bux.BudArgumentError(
                'Seems like non-existing path {}'.format(layer))

        self.bud['slices'].append(self.sliceMaker.make(layer))
        # self.parseEntry(layer)

    def parse(self, entries):
        if not isinstance(entries, list):
            entries = [entries]

        for entry in entries:
            self.interpret(entry)
        return self.bud
