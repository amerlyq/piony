#!/usr/bin/env python3
# vim: fileencoding=utf-8

import os
import sys
from collections import namedtuple
import yaml


class BudParser:
    segment = namedtuple('SegmentCfg', ['name', 'action', 'tooltip'])

    def __init__(self):
        self.bud = {"slices": [
            {"rings": []}
        ]}

    def tooltip(self, action):
        return '<b>' + action + '</b>'

    def addSegment(self, seg):
        if isinstance(seg, dict):
            action = seg.get('action', None)
            name = seg.get('name', action)
            tooltip = seg.get('tooltip', self.tooltip(action))
        elif isinstance(seg, list):  # [action, name, tooltip]
            action = seg[0] if len(seg) > 0 else None
            name = seg[1] if len(seg) > 1 else action
            tooltip = seg[2] if len(seg) > 2 else self.tooltip(action)
        else:
            action = seg
            name = action
            tooltip = self.tooltip(action)

        return BudParser.segment(name, action, tooltip)

    def addRing(self, ring):
        return map(self.addSegment, ring)

    def addEntry(self, layer):
        if isinstance(layer, dict):
            if "segments" in layer:
                pass  # addRing
            if "rings" in layer:
                pass  # addSlice
            if "slices" in layer:
                pass  # mergeSlices
        elif isinstance(layer, list):
            if all(map(lambda i: isinstance(i, list), layer)):
                pass  # decorateRing, addSlice
            elif any(map(lambda i: isinstance(i, list), layer)):
                raise SyntaxError('Unsupported mixed slice')
            else:
                self.bud['slices'][-1]['rings'].append(self.addRing(layer))
                pass  # decorateSgmt, addRing
        else:
            raise SyntaxError('Bad slice format. Expected keys: ...')

    def read_entry(self, entry):
        if '-' == entry:
            layer = yaml.safe_load(sys.stdin)  # entry = sys.stdin.read()
        elif os.path.isfile(entry):            # && os.path.isabs(PATH)
            with open(entry, 'r') as f:
                layer = yaml.safe_load(f)      # entry = f.read()
        else:
            layer = yaml.safe_load(entry)
        self.addEntry(layer)

    def read_args(self, args):
        if not isinstance(args, list):
            self.read_entry(args)
        else:
            for arg in args:  # BUG: Why map don't works ?!
                self.read_entry(arg)
        if not self.bud['slices'][-1]['rings']:
            self.bud['slices'][-1]['rings'].append([])
        return self.bud
