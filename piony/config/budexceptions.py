class ParseError(Exception):
    """Base class for bud parsing exceptions."""
    pass


class MyError(ParseError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InputError(ParseError):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TransitionError(ParseError):
    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message
