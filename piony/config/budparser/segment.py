from collections import namedtuple

from .exceptions import BudSyntaxError


class SegmentMaker:
    """ 'a' or [..] or {..} -> {name:_, action:_, ...} """

    PS = "<i>Placeholder</i>"
    NM = 'Segment'
    KEYS = ('name', 'action', 'tooltip')
    SEG = namedtuple(NM, KEYS)
    # OR: NM = type(SEG).__name__; KEYS = SEG._fields

    def tooltip(self, action):
        return '<b>' + str(action) + '</b>' if action else None

    def fromList(self, seg):
        action = seg[0] if len(seg) > 0 else None
        name = seg[1] if len(seg) > 1 else action
        tooltip = seg[2] if len(seg) > 2 else self.tooltip(action)
        return (name, action, tooltip)

    def fromDict(self, seg):
        action = seg.get('action', None)
        name = seg.get('name', action)
        tooltip = seg.get('tooltip', self.tooltip(action))
        return (name, action, tooltip)

    def make(self, seg):
        if not seg:
            seg = ("", None, SegmentMaker.PS)
        elif isinstance(seg, str):
            seg = (seg, seg, self.tooltip(seg))
        elif isinstance(seg, list):
            seg = self.fromList(seg)  # Unused in general parsing path
        elif isinstance(seg, dict):
            seg = self.fromDict(seg)
        else:
            raise BudSyntaxError(
                'Impossible to derive {}'.format(SegmentMaker.NM))
        return SegmentMaker.SEG(*seg)
