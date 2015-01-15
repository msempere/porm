
class Field(object):
    def __init__(self, validators=[], unique=False, index=False):
        assert type(validators) == list
        self.validators = validators
        self.unique = unique
        self.index = index
        self.value = None

    def __str__(self):
        return self.value

    def __call__(self):
        return self.value

    def get(self):
        return self.__call__()

class StringField(Field):
    pass

class NumberField(Field):
    def __str__(self):
        return int(self.value)

    def __call__(self):
        return int(self.value)

    def get(self):
        return self.__call__()
