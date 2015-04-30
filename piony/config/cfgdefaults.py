#!/usr/bin/env python3
# vim: fileencoding=utf-8

from collections import OrderedDict


G_CONFIG_DEFAULT = OrderedDict((
    ('Bud', OrderedDict((
        ('default', './cfgs/krita.yml'),
    ))),
    ('Button', OrderedDict((
        ('text_scale', 0.64),
    ))),
    ('Window', OrderedDict((
        ('text_scale', 0.64),
        ('size', 360),
        ('no_tooltip', False),
    ))),
))
