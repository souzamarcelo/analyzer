from enumerates import Type
from parameter import Parameter
from configuration import Configuration
import random
import subprocess

class Scenario:
    def __init__(self):
        self.parameters = None
        self.instances = None
        self.command = None
        self.create()
    
    def create(self):
        self.parameters = []
        self.parameters.append(Parameter('algorithm', '--', Type.CATEGORICAL, ['as', 'mmas', 'eas', 'ras', 'acs']))
        self.parameters.append(Parameter('localsearch', '--localsearch', Type.CATEGORICAL, ['0', '1', '2', '3']))
        self.parameters.append(Parameter('alpha', '--alpha', Type.REAL, [0.0, 5.0]))
        self.parameters.append(Parameter('beta', '--beta', Type.REAL, [0.0, 10.0]))
        self.parameters.append(Parameter('rho', '--rho', Type.REAL, [0.01, 1.0]))
        self.parameters.append(Parameter('ants', '--ants', Type.INTEGER, [5, 100]))
        self.parameters.append(Parameter('q0', '--q0', Type.REAL, [0.0, 1.0], 'algorithm == \'acs\''))
        self.parameters.append(Parameter('rasrank', '--rasrank', Type.INTEGER, [1, 100], 'algorithm == \'ras\''))
        self.parameters.append(Parameter('elitistants', '--elitistants', Type.INTEGER, [1, 750], 'algorithm == \'eas\''))
        self.parameters.append(Parameter('nnls', '--nnls', Type.INTEGER, [5, 50], 'localsearch in [\'1\', \'2\', \'3\']'))
        self.parameters.append(Parameter('dlb', '--dlb', Type.CATEGORICAL, ['0', '1'], 'localsearch in [\'1\', \'2\', \'3\']'))
        self.instances = []
        self.instances.append('./1000-1.tsp')
        self.command = './acotsp --quiet -r 1 -t 10 --seed <seed> -i <instance> <configuration>'

    def parse(self, configuration):
        text_config = ''
        for param in configuration.parameters:
            if configuration.parameters[param] is not None:
                text_config += ' ' + param.command + ('' if param.name == 'algorithm' else ' ') + str(configuration.parameters[param])
        return text_config.strip()

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

    def run(self, configuration, instance):
        text_config = self.parse(configuration)
        seed = str(random.randint(1, 999999))
        command = self.command
        command = command.replace('<seed>', seed)
        command = command.replace('<instance>', instance)
        command = command.replace('<configuration>', text_config)
        result = subprocess.run(command, stdout = subprocess.PIPE, shell = True)
        result = result.stdout.decode('utf-8')
        result = result.replace('\n', ';')
        result = result if result[-1] != ';' else result[:-1]
        result = int(result.split(';')[-1].split(':')[-1])
        return result