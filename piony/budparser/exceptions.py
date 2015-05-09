class PionyError(Exception):
    """Base class for bud parsing exceptions."""
    pass


class BudError(PionyError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(" ".join((self.value + '. ') if self.value else '',
                             'Expected keys: segments, rings, slices'))


class BudArgumentError(BudError):
    pass


class BudSyntaxError(BudError):
    pass


class InputError(PionyError):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TransitionError(PionyError):
    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message
