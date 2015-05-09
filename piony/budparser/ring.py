import piony.budparser.exceptions as bux

from piony.common import lst_isinstance
from piony.budparser.segment import SegmentMaker


class RingMaker:
    """ [..]/[{..}..]/{segments:[..],...} -> {segments:_} """

    NM = 'Ring'
    segmentMaker = SegmentMaker()

    def fromList(self, ring):
        if not all(lst_isinstance(ring, (str, dict))):
            raise bux.BudSyntaxError(
                'Unsupported mixed {}'.format(RingMaker.NM))
        return ring

    def fromDict(self, ring):
        if 'segments' not in ring:
            raise bux.BudSyntaxError(
                'Invalid {} format'.format(RingMaker.NM))
        elif len(ring) > 1:
            raise bux.BudSyntaxError(
                '{} contains odd keywords'.format(RingMaker.NM))
        ring = ring['segments']
        return ring

    def make(self, ring):
        if not ring:
            ring = []
        elif isinstance(ring, list):
            ring = self.fromList(ring)
        elif isinstance(ring, dict):
            ring = self.fromDict(ring)
        else:
            raise bux.BudArgumentError(
                'Impossible to derive {}'.format(RingMaker.NM))

        lst = map(self.segmentMaker.make, ring)
        return {"segments": list(lst)}
