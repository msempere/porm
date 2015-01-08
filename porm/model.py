import redis
from validators import ValidatorException
from fields import Field

class ModelException(Exception):
    pass

class Model(object):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.__dict__['connection'] = redis.StrictRedis(host=host, port=port, db=db)

    def __setattr__(self, name, value):
        if getattr(self, name, None):
            if len(getattr(self, name).validators) == 0:
                self.__dict__[name] = getattr(self, name)
                getattr(self, name).value = value

            for v in getattr(self, name).validators:
                v.value = value
                if v.validate():
                    self.__dict__[name] = getattr(self, name)
                    getattr(self, name).value = value
                else:
                    raise ValidatorException("%s could not validate '%s'"%(v.__class__.__name__, value))
        else:
            raise ModelException("'%s' is not a field member of '%s'"%(name, self.__class__.__name__))

    def save(self):
        if not self.has_index():
            raise ModelException("'%s' does not have a index key"%(self.__class__.__name__))
        else:
            args = {}
            index = None
            for element in self.__dict__:
                obj = getattr(self, element)
                if isinstance(obj, Field):
                    if obj.index:
                        index = str(obj.value)
                    else:
                        args[element] = obj.value
            self.connection.hmset(index, args)


    def has_index(self):
        for element in self.__dict__:
            obj = getattr(self, element)
            if isinstance(obj, Field):
                if getattr(self, element).index:
                    return True
        return False


