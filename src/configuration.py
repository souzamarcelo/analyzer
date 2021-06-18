from enumerates import Type

class Configuration:
    def __init__(self, _parameters, values = None):
        self.parameters = {}
        for index in range(len(_parameters)):
            self.parameters[_parameters[index].name] = (_parameters[index], None if values is None else values[index])

    def get_id(self):
        return ','.join([str(v[1]) for v in self.parameters.values()])

    def copy(self):
        return Configuration([self.parameters[element][0] for element in self.parameters], [self.parameters[element][1] for element in self.parameters])

    def param_valid(self, param):
        conditions = param.conditions
        value = self.parameters[param.name][1]
        if conditions != '':
            for name in self.parameters:
                conditions = conditions.replace(name + ' ', 'self.parameters[\'' + name + '\'][1] ')
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
        for param_name in self.parameters:
            if not self.param_valid(self.parameters[param_name][0]): return False
        return True

    def set_value(self, param, new_value):
        if isinstance(param, str): param = self.parameters[param][0]
        old_value = self.parameters[param.name][1]
        self.parameters[param.name] = (param, new_value)
        return old_value

    def change_activates(self, param, new_value):
        old_value = self.set_value(param, new_value)
        activations = []
        for param_name in self.parameters:
            if param.name != param_name and self.parameters[param_name][1] is None:
                parameter = self.parameters[param_name][0]
                conditions = parameter.conditions
                for name in self.parameters:
                    conditions = conditions.replace(name + ' ', 'self.parameters[\'' + name + '\'][1] ')
                if conditions == '' or eval(conditions): activations.append(parameter)
        self.set_value(param, old_value)
        return activations

    def change_deactivates(self, param, new_value):
        old_value = self.set_value(param, new_value)
        deactivations = []
        for param_name in self.parameters:
            if param.name != param_name and self.parameters[param_name][1] is not None:
                parameter = self.parameters[param_name][0]
                conditions = parameter.conditions
                if conditions != '':
                    for name in self.parameters:
                        conditions = conditions.replace(name + ' ', 'self.parameters[\'' + name + '\'][1] ')
                    if not eval(conditions): deactivations.append(parameter)
        self.set_value(param, old_value)
        return deactivations

    def __str__(self):
        return self.get_id()

    def __repr__(self):
        return self.__str__()