from collections import namedtuple

import piony.budparser.exceptions as bux


class SegmentMaker:
    """ a/[..]/{..} -> {name:_, action:_, ...} """

    segment = namedtuple('SegmentCfg', ['name', 'action', 'tooltip'])
    # KEY = segment('name', 'action', 'tooltip')

    def tooltip(self, action):
        return '<b>' + action + '</b>'

    def fromList(self, seg):
        action = seg[0] if len(seg) > 0 else None
        name = seg[1] if len(seg) > 1 else action
        tooltip = seg[2] if len(seg) > 2 else self.tooltip(action)
        return SegmentMaker.segment(name, action, tooltip)

    def fromDict(self, seg):
        action = seg.get('action', None)
        name = seg.get('name', action)
        tooltip = seg.get('tooltip', self.tooltip(action))
        return SegmentMaker.segment(name, action, tooltip)

    def make(self, seg):
        if not seg:
            return SegmentMaker.segment("", None, "<i>Placeholder</i>")
        elif isinstance(seg, str):
            return SegmentMaker.segment(seg, seg, self.tooltip(seg))
        elif isinstance(seg, list):
            return self.fromList(seg)
        elif isinstance(seg, dict):
            return self.fromDict(seg)
        else:
            raise bux.BudSyntaxError('Impossible to derive Segment')
