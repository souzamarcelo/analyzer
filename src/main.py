from enumerates import Type
from parameter import Parameter
from configuration import Configuration
from functions import get_configuration_space

p1 = Parameter('p1', '--p1 ', Type.CATEGORICAL, ['a', 'b'])
p2 = Parameter('p2', '--p2 ', Type.INTEGER, [1, 2]) # TODO: check case of float limits
parameters = [p1, p2]

configuration_space = get_configuration_space(parameters)
print(configuration_space)