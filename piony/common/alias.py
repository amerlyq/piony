# def xstr(s):  # Returns empty string even if None
#     return '' if s is None else str(s)


def any_are(lst, ptype):  # ptype -- can be tuple
    return any(map(lambda i: isinstance(i, ptype), lst))


def all_are(lst, ptype):  # ptype -- can be tuple
    return all(map(lambda i: isinstance(i, ptype), lst))


def any_in(lst, dst):
    return any(k in dst for k in list(lst))


def all_in(lst, dst):
    return all(k in dst for k in list(lst))
