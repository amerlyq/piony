from piony.exceptions import PionyError


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
