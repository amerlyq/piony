import os
import sys
import yaml
from collections import OrderedDict

from piony.exceptions import InputError


def init():
    yaml.add_constructor(
        'tag:yaml.org,2002:map',
        lambda ldr, node: OrderedDict(ldr.construct_pairs(node)),
        Loader=yaml.SafeLoader)
    yaml.add_representer(
        OrderedDict,
        lambda dmp, data: dmp.represent_sequence(
            'tag:yaml.org,2002:map', list(data.items())),
        Dumper=yaml.SafeDumper)


def load(entry):
    if not entry:
        obj = None

    elif '-' == entry:
        obj = yaml.safe_load(sys.stdin)  # entry = sys.stdin.read()

    elif os.path.isfile(entry):            # && os.path.isabs(PATH)
        with open(entry, 'r') as f:
            obj = yaml.safe_load(f)      # entry = f.read()
    else:
        obj = yaml.safe_load(entry)
        if obj and not isinstance(obj, (list, OrderedDict)):
            raise InputError('Seems like non-existing path: {}'.format(obj))
    return obj


def save(obj, path):
    if '-' == path:
        yaml.safe_dump(obj, stream=sys.stdout)
    else:
        with open(path, 'w') as f:
            yaml.safe_dump(obj, stream=f)
