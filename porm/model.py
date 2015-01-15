import redis
from validators import ValidatorException
from fields import Field
import copy

class ModelException(Exception):
    pass

class Model(object):
    connection = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    def __init__(self, host='127.0.0.1', port=6379, db=0, prefix=''):
        self.__dict__['connection'] = self.__class__.connection = redis.StrictRedis(host=host, port=port, db=db)
        self.__dict__['prefix'] = self.__class__.prefix = prefix
        self.__dict__['index'] = '%s:%s' % (prefix, self.__class__.__name__) if prefix else self.__class__.__name__
        self.__dict__['has_index'] = False


    def __setattr__(self, name, value):
        obj = getattr(self, name, None)

        # check if the attribute was defined previously in the class
        if obj:
            if isinstance(obj, Field): # only for Fields
                validators = getattr(self, name).validators

                if len(validators) > 0: # there are validators to evaluate before assignation
                    for validator in validators:
                        validator.value = value

                        if not validator.validate():
                            raise ValidatorException("%s could not validate '%s'"%(validator.__class__.__name__, value))

                # if all validators are correct then assignation can be performed
                self.__dict__[name] = copy.deepcopy(self.__class__.__dict__[name])
                self.__dict__[name].value = value

                if obj.index: # index updated with a new index
                    index = getattr(self, 'index')
                    self.__dict__['index'] = '%s:%s' % (index, str(value))
                    self.__dict__['has_index'] = True
        else:
            raise ModelException("'%s' is not a field member of '%s'"%(name, self.__class__.__name__))


    # saves the model filled
    def save(self):
        if not self.has_index:
            raise ModelException("'%s' does not have a index key"%(self.__class__.__name__))
        else:
            args = {}

            for element in self.__dict__:
                obj = getattr(self, element)
                if isinstance(obj, Field):
                    if obj.value and not obj.index: # avoiding empty values or indexes
                        args[element] = obj.value
            try:
                self.connection.hmset(self.index, args)
                return True
            except:
                return False


    @classmethod
    def find(cls, key):
        try:
            _key = '%s%s:%s' % (('%s:' % cls.prefix if cls.prefix else ''), cls.__name__, key)
        except:
            _key = '%s:%s' % (cls.__name__, key)
        got = cls.connection.hgetall(_key)
        new = cls()

        # if exists we fill a object with all the information from Redis
        if got:
            for element in cls.__dict__:
                obj = getattr(cls, element)
                if isinstance(obj, Field):
                    new.__dict__[element] = copy.deepcopy(obj)

                    if obj.index:
                        new.__dict__[element].value = key
                    else:
                        new.__dict__[element].value = got[element]
        return new


    # removes the data for that model
    def free(self):
        if self.has_index:
            if self.index:
                try:
                    self.connection.delete(self.index)
                    return True
                except:
                    return False
        raise ModelException("'%s' does not have a index key"%(self.__class__.__name__))


    # checks if a model already exists
    def exists(self):
        if self.has_index:
            if self.index:
                return self.connection.exists(self.index) > 0
        raise ModelException("'%s' does not have a index key"%(self.__class__.__name__))

    def __str__(self):
        attrs = {}
        for element in self.__dict__:
            obj = getattr(self, element)
            if isinstance(obj, Field):
                attrs[element] = obj.get()
        return str(attrs)


