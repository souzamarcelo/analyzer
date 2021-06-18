from enumerates import Type
from parameter import Parameter
from configuration import Configuration

class TestCase1:
    def __init__(self):
        self.name = 'TestCase 1'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['x', 'y'])
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 1
        if configuration.parameters['p2'][1] == 'x': return 1
        return 0

class TestCase2:
    def __init__(self):
        self.name = 'TestCase 2'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['x', 'y'], 'p1 == \'b\'')
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 1
        if configuration.parameters['p2'][1] == 'x': return 1
        return 0

class TestCase2_1:
    def __init__(self):
        self.name = 'TestCase 2.1'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b', 'c']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['x', 'y'], 'p1 == \'b\' or p1 == \'c\'')
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 1
        if configuration.parameters['p2'][1] == 'x': return 1
        return 0

class TestCase2_2:
    def __init__(self):
        self.name = 'TestCase 2.2'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b', 'c']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['x', 'y'], 'p1 == \'b\' or p1 == \'c\'')
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 1
        if configuration.parameters['p1'][1] == 'b' and configuration.parameters['p2'][1] == 'y': return 1
        if configuration.parameters['p1'][1] == 'c' and configuration.parameters['p2'][1] == 'x': return 1
        return 0

class TestCase2_3:
    def __init__(self):
        self.name = 'TestCase 2.3'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b', 'c']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['x', 'y'], 'p1 == \'b\' or p1 == \'c\'')
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 0
        if configuration.parameters['p2'][1] == 'x': return 2
        return 1

class TestCase3:
    def __init__(self):
        self.name = 'TestCase 3'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['x', 'y'], 'p1 == \'b\'')
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 1
        return 0

class TestCase4ab:
    def __init__(self):
        self.name = 'TestCase 4 {a, b}'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b']),
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 0
        return 1

class TestCase4abcd:
    def __init__(self):
        self.name = 'TestCase 4 {a, b, c, d}'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b', 'c', 'd']),
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 0
        return 1

class TestCase5:
    def __init__(self):
        self.name = 'TestCase 5'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['c', 'd']),
            Parameter('p3', '--p3 ', Type.CATEGORICAL, ['x', 'y'], 'p1 == \'b\' and p2 == \'d\'')
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 1
        return 0

class TestCase6:
    def __init__(self):
        self.name = 'TestCase 6'
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['c', 'd']),
            Parameter('p3', '--p3 ', Type.CATEGORICAL, ['x', 'y'], 'p1 == \'b\' and p2 == \'d\'')
        ]

    def evaluate(self, configuration):
        if configuration.parameters['p1'][1] == 'a': return 0
        if configuration.parameters['p2'][1] == 'd' and configuration.parameters['p3'][1] == 'x': return 1
        if configuration.parameters['p2'][1] == 'd' and configuration.parameters['p3'][1] == 'y': return -1
        return 0