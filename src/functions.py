import itertools
from configuration import Configuration

def get_configuration_space(parameters):
    space = []
    all_values = [parameter.get_values() for parameter in parameters]
    for values in itertools.product(*all_values):
        space.append(values)
    return list(dict.fromkeys(space))

# TODO: filter configuration space to keep only valid configurations
# TODO: implement evaluation function