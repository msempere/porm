import redis
from porm.model import Model
from porm.validators import StringValidator, RegexValidator, ValidatorException
from porm.fields import StringField
from unittest import TestCase
import pytest

class TestCache(TestCase):

    def test_basic_saving(self):
        class User(Model):
            name = StringField(default='',
                               index=True,
                               validators= [
                                            StringValidator(min_length=0, max_length=20),
                                            RegexValidator('^P')
                                            ])
            surname = StringField()

        user = User()
        user.name = "Peter"
        user.surname = "Pan"
        user.save()

        connection = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        assert connection.hget('User:Peter', 'surname') == 'Pan'


    def test_basic_validation(self):
        class User(Model):
            name = StringField(default='',
                               index=True,
                               validators= [
                                            StringValidator(min_length=0, max_length=20),
                                            RegexValidator('^A')
                                            ])
            surname = StringField()

        with pytest.raises(ValidatorException):
            user = User()
            user.name = "Peter2"
            user.surname = "Pan2"

    def test_exists_key(self):
        class User(Model):
            name = StringField(default='',
                               index=True,
                               validators= [
                                            StringValidator(min_length=0, max_length=20)
                                            ])
            surname = StringField()

        user = User()
        user.name = "Peter2"
        user.surname = "Pan2"
        user.save()

        assert user.exists() == True

    def test_free_key(self):
        class User(Model):
            name = StringField(default='',
                               index=True,
                               validators= [
                                            StringValidator(min_length=0, max_length=20)
                                            ])
            surname = StringField()

        user = User()
        user.name = "Peter3"
        user.surname = "Pan3"
        user.save()
        assert user.exists() == True
        user.free()
        assert user.exists() == False




