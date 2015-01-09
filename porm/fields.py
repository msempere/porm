
class Field(object):
    def __init__(self, validators=[], unique=False, index=False):
        self.validators = validators
        self.unique = unique
        self.index = index
        self.value = None

    def __str__(self):
        return self()

    def __call__(self):
        return self.value

    def get(self):
        return self.__call__()

class StringField(Field):
    pass

class NumberField(Field):
    pass
