import sys
from os import path as fs


def expand_pj(path, pjd=fs.dirname(fs.abspath(sys.argv[0]))):
    if isinstance(path, str) and path.startswith(":/"):
        path = fs.join(pjd, path[2:])
    return path
