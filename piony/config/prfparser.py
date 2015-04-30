#!/usr/bin/env python3
# vim: fileencoding=utf-8

import yaml
from collections import namedtuple


class ProfileParser:
    segment = namedtuple('SegmentCfg', ['name', 'action', 'tooltip'])

    def tooltip(self, action):
        return '<b>' + action + '</b>'

    def parseEntry(self, entry):
        if isinstance(entry, dict):
            action = entry.get('action', None)
            name = entry.get('name', action)
            tooltip = entry.get('tooltip', self.tooltip(action))
        elif isinstance(entry, list):  # [action, name, tooltip]
            action = entry[0] if len(entry) > 0 else None
            name = entry[1] if len(entry) > 1 else action
            tooltip = entry[2] if len(entry) > 2 else self.tooltip(action)
        else:
            action = entry
            name = action
            tooltip = self.tooltip(action)

        return ProfileParser.segment(name, action, tooltip)

    def parseRing(self, cfg):
        return map(self.parseEntry, cfg)

    def read_file(self, path):
        with open(path) as prof_file:
            prof = yaml.safe_load(prof_file)
        return self.parseRing(prof)
