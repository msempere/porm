# PORM [![Build Status](https://travis-ci.org/msempere/porm.svg?branch=master)] (http://travis-ci.org/msempere/porm)

Python Redis ORM

## Setup:
```
pip install -r requirements.txt
```
```
python setup.py install
```

## Usage example

```python
from porm.model import Model
from porm.validators import StringValidator, RegexValidator
from porm.fields import StringField

class User(Model):
    name = StringField(default='', 
                        index=True,
                        validators= [
                                        StringValidator(min_length=0, max_length=20),
                                        RegexValidator('^P')
                                    ])
                                
    surname = StringField(validators=[
                                        StringValidator(min_length=0, max_length=20),
                                    ])

user = User()
user.name = "Peter"
user.surname = "Pan"
user.save()

user.free() # returns True
user.exist() # return False
```
