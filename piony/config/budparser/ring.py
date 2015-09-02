from piony.common.alias import all_are, any_in, all_in
from .exceptions import BudSyntaxError, BudArgumentError
from .segment import SegmentMaker


class RingMaker:
    """ [..] or [{..}..] or {segments:[..],...} -> {segments:_} """

    NM = 'Ring'
    KEYS = ('segments',)
    segmentMaker = SegmentMaker()

    def fromList(self, ring):
        if not all_are(ring, (str, dict)):
            raise BudSyntaxError(
                'Unsupported mixed {}'.format(RingMaker.NM), RingMaker.KEYS)
        return ring

    def fromDict(self, ring):
        if not any_in(RingMaker.KEYS, ring):
            if any_in(ring, self.segmentMaker.KEYS):
                return [ring]
            else:
                raise BudSyntaxError(
                    'Invalid {} format'.format(RingMaker.NM), ring)
        elif not all_in(ring, RingMaker.KEYS):
            raise BudSyntaxError(
                '{} contains odd keywords'.format(RingMaker.NM), RingMaker.KEYS)
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
            raise BudArgumentError(
                'Impossible to derive {}'.format(RingMaker.NM))

        lst = map(self.segmentMaker.make, ring)
        return {"segments": list(lst)}
