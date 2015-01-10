![Logo](http://i.imgur.com/xOJFRp4.png)

Python Redis ORM [![Build Status](https://travis-ci.org/msempere/porm.svg?branch=master)](https://travis-ci.org/msempere/porm) [![Requirements Status](https://requires.io/github/msempere/porm/requirements.svg?branch=master)](https://requires.io/github/msempere/porm/requirements/?branch=master)


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
from porm.validators import StringValidator, RegexValidator, EmailValidator, NumberValidator, LenghValidator
from porm.fields import StringField

class User(Model):
    name = StringField(index=True, validators= [
                                                StringValidator(),
                                                LenghValidator(min_length=0, max_length=20)
                                                RegexValidator('^P')
                                                ])
                                
    surname = StringField(validators=[
                                        StringValidator(),
                                        LenghValidator(min_length=0, max_length=20)
                                    ])
                                    
    age = NumberField(validators=[
                                     RangeValidator(min=0, max=120)
                                ])
    
    email = StringField(validators=[
                                        NumberValidator(),
                                        EmailValidator()
                                    ])
    
    ip = StringField(validators=[
                                    IPAddressValidator(ipv4=True)
                                    ])

user = User()
user.name = 'Peter'
user.surname = 'Pan'
user.age = 15
user.email = 'peter@pan.com'
user.ip = '127.0.0.1'

user.save() # returns True
user.free() # returns True
user.exist() # return False
```

## Saving data
```python
>>> user = User()
>>> user.name = 'Peter'
>>> user.email = 'peter@pan.com
>>> user.save()
True
```

## Retrieving data

```python
>>> found_user = User.find('Peter')
>>> found_user.email
'peter@pan.com'
```

## Validators

 * StringValidator (str)
 * NumberValidator (int, float)
 * EmailValidator (str)
 * RegexValidator (str)
 * EqualToValidator (str, int, float)
 * NumberRangeValidator (int, float)
 * LenghValidator (str)
 * IPAddressValidator (str) (Support for ipv4 and ipv6)
