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
from porm import model, validators, fields

class User(Model):
    name = fields.StringField(default='', 
                                index=True,
                                validators= [validators.StringValidator(min_length=0,
                                                                        max_length=20)])
                                
    surname = fields.StringField(validators=[validators.StringValidator(min_length=0, 
                                                                        max_length=20)])

user = User()
user.name = "Peter"
user.surname = "Pan"
user.save()
```
