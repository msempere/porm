import redis
from validators import ValidatorException
from fields import Field

class ModelException(Exception):
    pass

class Model(object):
    def __init__(self, host='127.0.0.1', port=6379, db=0, prefix=''):
        self.__dict__['connection'] = redis.StrictRedis(host=host, port=port, db=db)
        self.__dict__['prefix'] = prefix
        self.__dict__['index'] = '%s:%s' % (prefix, self.__class__.__name__) if prefix else self.__class__.__name__

    def __setattr__(self, name, value):
        if getattr(self, name, None):
            obj = getattr(self, name)
            if isinstance(obj, Field):
                if len(getattr(self, name).validators) == 0:
                    self.__dict__[name] = getattr(self, name)
                    getattr(self, name).value = value
                else:
                    for v in getattr(self, name).validators:
                        v.value = value
                        if not v.validate():
                            raise ValidatorException("%s could not validate '%s'"%(v.__class__.__name__, value))
                    self.__dict__[name] = getattr(self, name)
                    getattr(self, name).value = value
        else:
            raise ModelException("'%s' is not a field member of '%s'"%(name, self.__class__.__name__))

    # saves the model filled
    def save(self):
        if not self.__has_index():
            raise ModelException("'%s' does not have a index key"%(self.__class__.__name__))
        else:
            args = {}
            self.__dict__['index'] = self.__get_index()

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

    # removes the data for that model
    def free(self):
        if self.index:
            try:
                self.connection.delete(self.index)
                return True
            except:
                return False
        else:
            raise ModelException("'%s' does not have a index key"%(self.__class__.__name__))

    def __get_index(self):
        index = ''
        for element in self.__dict__:
            obj = getattr(self, element)
            if isinstance(obj, Field):
                if getattr(self, element).index:
                    index = '%s:%s' % (str(obj.value), index) if index else str(obj.value)
        return None if not index else '%s:%s' % (self.index, index)

    # checks if a model already exists
    def exists(self):
        if self.index:
            return self.connection.exists(self.index) > 0
        return False

    def __has_index(self):
        return True if self.__get_index() else False

