import piony.budparser.exceptions as bux

from piony.common import all_are, any_in, all_in
from piony.budparser.segment import SegmentMaker


class RingMaker:
    """ [..]/[{..}..]/{segments:[..],...} -> {segments:_} """

    NM = 'Ring'
    KEYS = ('segments',)
    segmentMaker = SegmentMaker()

    def fromList(self, ring):
        if not all_are(ring, (str, dict)):
            raise bux.BudSyntaxError(
                'Unsupported mixed {}'.format(RingMaker.NM))
        return ring

    def fromDict(self, ring):
        if not any_in(RingMaker.KEYS, ring):
            if any_in(ring, self.segmentMaker.KEYS):
                return [ring]
            else:
                raise bux.BudSyntaxError(
                    'Invalid {} format'.format(RingMaker.NM))
        elif not all(k in RingMaker.KEYS for k in list(ring)):
            raise bux.BudSyntaxError(
                '{} contains odd keywords'.format(RingMaker.NM))
        else:
            return ring['segments']

    def make(self, ring):
        if not ring:
            ring = []
        elif isinstance(ring, (list, tuple)):
            ring = self.fromList(ring)
        elif isinstance(ring, dict):
            ring = self.fromDict(ring)
        else:
            raise bux.BudArgumentError(
                'Impossible to derive {}'.format(RingMaker.NM))

        lst = map(self.segmentMaker.make, ring)
        return {"segments": list(lst)}
