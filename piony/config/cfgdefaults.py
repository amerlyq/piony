from collections import OrderedDict


G_CONFIG_DEFAULT = OrderedDict((
    ('DEFAULT', OrderedDict((
        ('text_scale', 1.0),
    ))),
    ('Bud', OrderedDict((
        ('default', './cfgs/krita.yml'),
        ('line_width', 2),
    ))),
    ('Button', OrderedDict((
        ('text_scale', 0.64),
    ))),
    ('System', OrderedDict((
        ('no_focus', False),
    ))),
    ('Window', OrderedDict((
        ('text_scale', 0.64),
        ('size', 360),
        ('no_tooltip', False),
    ))),
))
