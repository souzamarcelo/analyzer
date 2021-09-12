from enumerates import Type

class Configuration:
    def __init__(self, _parameters, values = None):
        self.parameters = {}
        for index in range(len(_parameters)):
            self.parameters[_parameters[index]] = None if values is None else values[index]

    def get_id(self):
        return ','.join([str(v) for v in self.parameters.values()])

    def copy(self):
        return Configuration([param for param in self.parameters], [self.parameters[param] for param in self.parameters])

    def get_value_by_name(self, param_name):
        for param in self.parameters:
            if param.name == param_name: return self.parameters[param]
        print('Error: Parameter not found [get_value_by_name]')
        exit(1)

    def param_valid(self, param):
        conditions = param.conditions
        value = self.parameters[param]
        if conditions != '':
            for p in self.parameters:
                if p.name in conditions and self.parameters[p] is None:
                    conditions = 'False'
                    break
                else:
                    conditions = conditions.replace(p.name + ' ', 'self.get_value_by_name(\'' + p.name + '\') ')
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
        for param in self.parameters:
            if not self.param_valid(param): return False
        return True

    def set_value(self, param, new_value):
        old_value = self.parameters[param]
        self.parameters[param] = new_value
        return old_value

    def change_activates(self, param, new_value):
        old_value = self.set_value(param, new_value)
        activations = []
        for p in self.parameters:
            if param.name != p.name and self.parameters[p] is None:
                conditions = p.conditions
                for p2 in self.parameters:
                    if p2.name in conditions and self.parameters[p2] is None:
                        conditions = 'False'
                        break
                    else:
                        conditions = conditions.replace(p2.name + ' ', 'self.get_value_by_name(\'' + p2.name + '\') ')
                if conditions == '' or eval(conditions): activations.append(p)
        self.set_value(param, old_value)
        return activations

    def change_deactivates(self, param, new_value):
        old_value = self.set_value(param, new_value)
        deactivations = []
        for p in self.parameters:
            if param.name != p.name and self.parameters[p] is not None:
                conditions = p.conditions
                if conditions != '':
                    for p2 in self.parameters:
                        if p2.name in conditions and self.parameters[p2] is None:
                            conditions = 'False'
                            break
                        else:
                            conditions = conditions.replace(p2.name + ' ', 'self.get_value_by_name(\'' + p2.name + '\') ')
                    if not eval(conditions):
                        deactivations.append(p)
                        deactivations.extend(self.change_deactivates(p, None))
        self.set_value(param, old_value)
        return deactivations

    def fix(self):
        for param in self.parameters:
            conditions = param.conditions
            if conditions != '':
                for p in self.parameters:
                    if p.name in conditions and self.parameters[p] is None:
                        conditions = 'False'
                        break
                    else:
                        conditions = conditions.replace(p.name + ' ', 'self.get_value_by_name(\'' + p.name + '\') ')
            if conditions != '' and not eval(conditions):
                self.parameters[param] = None

    def children(self, param, new_value):
        deactivations = self.change_deactivates(param, new_value)
        new_config = self.copy()
        new_config.set_value(param, new_value)
        for dparam in deactivations:
            new_config.set_value(dparam, None)
        #
        activations = new_config.change_activates(param, new_value)
        if len(activations) == 0:
                return [new_config] if new_config.is_valid() else []
        else:
            result = []
            for aparam in activations:
                for value in aparam.values:
                    result.extend(new_config.children(aparam, value))
        #
        filtered_result = []
        added = {}
        for child in result:
            if child.get_id() not in added:
                added[child.get_id()] = None
                filtered_result.append(child)
        return filtered_result

    def __str__(self):
        return self.get_id()

    def __repr__(self):
        return self.__str__()