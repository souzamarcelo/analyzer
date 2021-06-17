import itertools
from configuration import Configuration

def get_config_space(scenario):
    space = {}
    all_values = [parameter.get_values() for parameter in scenario.parameters]
    for element in all_values:
        element.append(None)
    for values in itertools.product(*all_values):
        c = Configuration(scenario.parameters, values)
        if c.is_valid(): space[c.id] = (c, None)
    return space

def evaluate_config_space(scenario, config_space):
    for config in config_space:
        result = scenario.evaluate(config_space[config][0])
        config_space[config] = (config_space[config][0], result)
    return config_space