class PionyError(Exception):
    """Base class for this program exceptions."""
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
