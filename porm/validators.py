import re


class ValidatorException(Exception):
    pass

class Validator(object):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class StringValidator(Validator):
    def validate(self):
        return True if type(self.value) == str else False

class NumberValidator(Validator):
    def validate(self):
        return True if (type(self.value) == int or type(self.value) == float) else False


class LengthValidator(Validator):
    def __init__(self, min_length, max_length):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self):
        if len(self.value) > self.max_length or len(self.value) < self.min_length:
            return False
        else:
            return True


class EqualToValidator(Validator):
    def __init__(self, val):
        self.val = val

    def validate(self):
        return True if self.val == self.value else False


class NumberRangeValidator(Validator):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def validate(self):
        if (type(self.value) != int and type(self.value) != float) or self.value > self.max or self.value < self.min:
            return False
        else:
            return True


class RegexValidator(Validator):
    def __init__(self, regex, flags=0):
        self.regex = regex
        self.flags = flags

    def validate(self):
        if isinstance(self.regex, basestring) and self.value:
            regex = re.compile(self.regex, self.flags)
            match = regex.match(self.value or '')

            if match:
                return True
        return False


class EmailValidator(RegexValidator):
    def __init__(self):
        super(EmailValidator, self).__init__(r'^.+@([^.@][^@]+)$', re.IGNORECASE)

