
class Field(object):
    def __init__(self):
        pass

class StringField(Field):
    def __init__(self, default=None, validators=[], unique=False, index=False):
        self.default = default
        self.validators = validators
        self.unique = unique
        self.index = index
        self.value = None

    def __str__(self):
        return str(self.value)
