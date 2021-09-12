from enumerates import Type
from parameter import Parameter
from configuration import Configuration
import random
import subprocess

class Artificial:
    def __init__(self):
        self.parameters = None
        self.instances = None
        self.command = None
        self.create()

    def create(self):
        self.parameters = []
        self.parameters.append(Parameter('x1', '-x1', Type.CATEGORICAL, ['1', '2']))
        self.parameters.append(Parameter('x2', '-x2', Type.CATEGORICAL, ['1', '2', '3']))
        self.parameters.append(Parameter('x3', '-x3', Type.CATEGORICAL, ['0', '1']))
        self.parameters.append(Parameter('x4', '-x4', Type.REAL, [0, 1], 'x2 == \'2\''))
        self.parameters.append(Parameter('x5', '-x5', Type.INTEGER, [1, 10]))
        self.instances = []
        self.instances.append('x')
        self.command = ''

    def parse(self, configuration):
        return ''

    def get_random_configuration(self):
        values = []
        for param in self.parameters:
            if param.type == Type.CATEGORICAL:
                values.append(random.choice(param.domain))
            elif param.type == Type.INTEGER:
                values.append(random.randint(param.domain[0], param.domain[1]))
            elif param.type == Type.REAL:
                values.append(round((((param.domain[1] - param.domain[0]) * random.random()) + param.domain[0]), 2))
        c = Configuration(self.parameters, values)
        c.fix()        
        return c
        
    def get_instance_set(self):
        return self.instances

    def dependents(self, parameter):
        result = []
        for param in self.parameters:
            if parameter.name in param.conditions:
                result.append(param)
        return result

    def weight(self, parameter, configuration):
        weights = {
            'x1': 2,
            'x2': 2,
            'x3': 2,
            'x4': 2,
            'x5': 2
        }
        targets = {
            'x1': ['1', '2'],
            'x2': ['1', '2', '3'],
            'x3': ['0', '1'],
            'x4': [0, 0.5],
            'x5': [1, 10]
        }
        #
        if configuration.parameters[parameter] is None: return 0
        w = 1
        if parameter.type == Type.CATEGORICAL:
            if configuration.parameters[parameter] in targets[parameter.name]:
                w = weights[parameter.name]
        else:
            if configuration.parameters[parameter] >= targets[parameter.name][0] and configuration.parameters[parameter] <= targets[parameter.name][1]:
                w = weights[parameter.name]
        #
        for param in self.dependents(parameter):
            if configuration.parameters[param] is not None:
                w = w * self.weight(param, configuration)
        return w

    def run(self, configuration, instance = None):
        bases = {
            'x1': 10,
            'x2': 10,
            'x3': 10,
            'x4': 0,
            'x5': 10
        }
        result = 0
        for param in self.parameters:
            if configuration.parameters[param] is not None:
                result += bases[param.name] * self.weight(param, configuration)
        return result