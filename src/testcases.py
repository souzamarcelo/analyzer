from enumerates import Type
from parameter import Parameter
from configuration import Configuration

class TestCase1:
    def __init__(self):
        self.parameters = [
            Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b']),
            Parameter('p2', '--p2 ', Type.CATEGORICAL, ['x', 'y'])
        ]

    def evaluate(self, configuration):
        if configuration.name_value['p1'] == 'a': return 1
        if configuration.name_value['p2'] == 'x': return 1
        return 0