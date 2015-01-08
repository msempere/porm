import redis
from porm.model import Model
from porm.validators import StringValidator
from porm.fields import StringField
from unittest import TestCase

class TestCache(TestCase):

    def test_basic_saving(self):
        class User(Model):
            name = StringField(default='', index=True, validators=[StringValidator(min_length=0, max_length=20)])
            surname = StringField()

        user = User()
        user.name = "Peter"
        user.surname = "Pan"
        user.save()

        connection = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        assert connection.hget('Peter', 'surname') == 'Pan'





