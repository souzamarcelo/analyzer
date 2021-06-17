from enumerates import Type

class Configuration:
    def __init__(self, parameters, values = None):
        self.param_value = {}
        self.name_value = {}
        for index in range(len(parameters)):
            self.param_value[parameters[index]] = None if values is None else values[index]
            self.name_value[parameters[index].name] = None if values is None else values[index]
        self.id = ','.join([str(v) for v in self.param_value.values()])

    def param_valid(self, param):
        conditions = param.conditions
        value = self.param_value[param]
        
        if conditions != '':
            for name in self.name_value:
                conditions = conditions.replace(name + ' ', 'self.name_value[\'' + name + '\'] ')
                if not eval(conditions) and value is not None: return False
                if eval(conditions) and value is None: return False
        else:
            if value is None: return False

        if value is not None:
            if param.type == Type.INTEGER:
                return isinstance(value, int) and value >= param.domain[0] and value <= param.domain[1]
            if param.type == Type.REAL:
                return isinstance(value, float) and value >= param.domain[0] and value <= param.domain[1]
            if param.type == Type.CATEGORICAL:
                return isinstance(value, str) and value in param.domain
        
        return True

    def is_valid(self):
        name_value = {}
        for param in self.param_value:
            if not self.param_valid(param): return False
        return True

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.__str__()