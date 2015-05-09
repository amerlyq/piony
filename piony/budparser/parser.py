import os
import sys
import yaml

import piony.budparser.exceptions as bux
from piony.budparser.ring import RingMaker
from piony.budparser.slice import SliceMaker


class BudMaker:
    """ {slices:[..],...} -> {slices:_} """

    sliceMaker = SliceMaker()

    def make(self, bud):

        lst = map(self.sliceMaker.make, bud)
        return {"slices": list(lst)}


class BudParser:
    ringMaker = RingMaker()
    sliceMaker = SliceMaker()

    def __init__(self):
        self.default()

    def default(self):
        self.bud = {"slices": [{"rings": []}]}
        return self.bud

    def parseEntry(self, layer):
        if not layer:  # Empty buds are valid!
            pass
        elif isinstance(layer, dict):   # Long format for one entry
            self.bud['slices'].append(self.sliceMaker.make(layer))
        elif isinstance(layer, list):   # Short slice format
            self.bud['slices'][-1]['rings'].append(
                self.ringMaker.make(layer))
        else:
            raise bux.BudSyntaxError('Bad slice format')

    def interpret(self, entry):
        if '-' == entry:
            layer = yaml.safe_load(sys.stdin)  # entry = sys.stdin.read()
        elif os.path.isfile(entry):            # && os.path.isabs(PATH)
            with open(entry, 'r') as f:
                layer = yaml.safe_load(f)      # entry = f.read()
        else:
            layer = yaml.safe_load(entry)
        self.parseEntry(layer)

    def parse(self, entries):
        if isinstance(entries, list):
            for entry in entries:
                self.interpret(entry)
        else:
            self.interpret(entries)

        if not self.bud['slices'][-1]['rings']:
            self.bud['slices'][-1]['rings'].append({"segments": []})

        return self.bud
