class PionyError(Exception):
    """Base class for bud parsing exceptions."""
    pass


class BudError(PionyError):
    pass


class BudArgumentError(BudError):
    pass


class BudSyntaxError(BudError):
    def __init__(self, value, keys=""):
        self.value = value
        self.keys = keys

    def __str__(self):
        return repr("{}. Expected keys: {}.".format(
            (self.value + '. ') if self.value else '', str(self.keys)))


class InputError(PionyError):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TransitionError(PionyError):
    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message
