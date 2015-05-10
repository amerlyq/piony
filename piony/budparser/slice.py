import piony.budparser.exceptions as bux

from piony.common import all_are, any_in, all_in
from piony.budparser.ring import RingMaker


class SliceMaker:
    """ [[..]..]/{rings:[..],...} -> {rings:_} """

    NM = 'Slice'
    KEYS = ('rings', 'corners')
    ringMaker = RingMaker()

    def fromList(self, layer):
        if not all_are(layer, (list, dict)):
            raise bux.BudSyntaxError(
                'Unsupported mixed {}'.format(SliceMaker.NM),
                SliceMaker.KEYS)
        return layer

    def fromDict(self, layer):
        if not any_in(SliceMaker.KEYS, layer):
            if any_in(layer, self.ringMaker.KEYS):
                return [layer]
            else:
                raise bux.BudSyntaxError(
                    'Invalid {} format'.format(SliceMaker.NM))
        elif not all_in(layer, SliceMaker.KEYS):
            raise bux.BudSyntaxError(
                '{} contains odd keywords'.format(SliceMaker.NM))
        else:
            return layer['rings']

    def make(self, layer):
        if not layer:
            layer = [[]]
        elif isinstance(layer, list):
            layer = self.fromList(layer)
        elif isinstance(layer, dict):
            layer = self.fromDict(layer)
        else:
            raise bux.BudArgumentError(
                'Impossible to derive {}'.format(SliceMaker.NM))

        lst = map(self.ringMaker.make, layer)
        return {"rings": list(lst)}
