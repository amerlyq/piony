import piony.budparser.exceptions as bux

from piony.common import lst_isinstance
from piony.budparser.ring import RingMaker


class SliceMaker:
    """ [[..]..]/{rings:[..],...} -> {rings:_} """

    NM = 'Slice'
    ringMaker = RingMaker()

    def fromList(self, layer):
        if not all(lst_isinstance(layer, (list, dict))):
            raise bux.BudSyntaxError(
                'Unsupported mixed {}'.format(SliceMaker.NM))
        return layer

    def fromDict(self, layer):
        if 'rings' not in layer:
            raise bux.BudSyntaxError(
                'Invalid {} format'.format(SliceMaker.NM))
        elif len(layer) > 1:
            raise bux.BudSyntaxError(
                '{} contains odd keywords'.format(SliceMaker.NM))
        layer = layer['rings']

    def make(self, layer):
        if not layer:
            layer = []
        elif isinstance(layer, list):
            layer = self.fromList(layer)
        elif isinstance(layer, dict):
            layer = self.fromDict(layer)
        else:
            raise bux.BudArgumentError(
                'Impossible to derive {}'.format(SliceMaker.NM))

        lst = map(self.ringMaker.make, layer)
        return {"rings": list(lst)}
