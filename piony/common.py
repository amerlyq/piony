#!/usr/bin/env python3
# vim: fileencoding=utf-8

from math import degrees, acos, cos, sin, radians, sqrt, fmod


def xstr(s):  # Returns empty string even if None
    return '' if s is None else str(s)


def lst_isinstance(lst, ptype):  # ptype -- can be tuple
    return map(lambda i: isinstance(i, ptype), lst)


def similar(x, y, estimate=0.001):  # Floats robust comparison
    if isinstance(x, list) and isinstance(y, list):
        return all([similar(xi, yi, estimate) for xi, yi in zip(x, y)])
    else:
        return abs(x-y) < estimate


# Closest modulus: angle={base+3, base+6} -> base
# Usage: if angle is close to 90: (math.fabs(a - iround(a, 90)) < da/2)
def iround(angle, base):
    return round(float(angle) / base) * base


def lrotate(lst, n):  # Rotate list left:  [1,2,3,4] -> [2,3,4,1]
    n = n % len(lst) if lst else 0
    return lst[n:] + lst[:n]


def char_range(c1, c2):
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)


## ----------
def degreeNorm(a):  # angle -> [0,360)
    return fmod((fmod(a, 360) + 360), 360)


def arcContains(a, da, c):  # angle := [a, a+da]
    return da >= degreeNorm(360 + c - degreeNorm(a))


def ra2xy(r, angle):  # Polar to cartesian:
    x = r * cos(radians(angle))
    y = r * sin(radians(angle))
    return [x, y]


def xy2ra(x, y):  # Cartesian to polar:
    r = sqrt(x*x + y*y)
    a = degrees(acos(x/r)) + (0 if y >= 0 else 180)
    return [r, a]
