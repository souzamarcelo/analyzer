from itertools import product
from configuration import Configuration

def get_config_space(scenario):
    space = {}
    all_values = [param.values.copy() for param in scenario.parameters]
    for element in all_values:
        element.append(None)
    for values in product(*all_values):
        c = Configuration(scenario.parameters, values)
        if c.is_valid(): space[c.get_id()] = (c, None)
    return space

def evaluate_config_space(scenario, config_space):
    for config in config_space:
        result = scenario.evaluate(config_space[config][0])
        config_space[config] = (config_space[config][0], result)
    return config_space

def children(config, param, new_value):
    deactivations = config.change_deactivates(param, new_value)
    new_config = config.copy()
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
                result.extend(children(new_config, aparam, value))
    #
    filtered_result = []
    added = {}
    for child in result:
        if child.get_id() not in added:
            added[child.get_id()] = None
            filtered_result.append(child)
    return filtered_result

def score(config_space, config, param, value):
    #print('====================================')
    #print('Config:', config)
    #print('Param:', param)
    #print('Value:', value)
    #print(config_space)
    configs = children(config, param, value)
    #print()
    #print(configs)
    #print('====================================')
    total = 0
    for config in configs:
        total += config_space[config.get_id()][1]
    return total / len(configs)

def globality_param(config_space, EPSILON, param):
    impacts = 0
    configs_active = 0
    for config_id in config_space:
        config = config_space[config_id][0]
        if config.parameters[param.name][1] is not None:
            configs_active += 1
            min_score = float('inf')
            max_score = float('-inf')
            for value in param.values:
                score_value = score(config_space, config, param, value)
                min_score = min(min_score, score_value)
                max_score = max(max_score, score_value)
            if (max_score - min_score > EPSILON): impacts += 1
    globality_all = impacts / len(config_space)
    globality_active = impacts / configs_active
    return globality_all, globality_active

def globality(scenario, config_space, EPSILON):
    params = scenario.parameters
    globality_params = {}
    for param in params:
        globality_params[param] = globality_param(config_space, EPSILON, param)
    return globality_params

def impact_param(config_space, param):
    total_max_impact = 0
    configs_active = 0
    for config_id in config_space:
        config = config_space[config_id][0]
        if config.parameters[param.name][1] is not None:
            configs_active += 1
            min_score = float('inf')
            max_score = float('-inf')
            for value in param.values:
                score_value = score(config_space, config, param, value)
                min_score = min(min_score, score_value)
                max_score = max(max_score, score_value)
            total_max_impact += max_score - min_score
    impact_all = total_max_impact / len(config_space)
    impact_active = total_max_impact / configs_active
    return impact_all, impact_active

def impact(scenario, config_space):
    params = scenario.parameters
    impact_params = {}
    for param in params:
        impact_params[param] = impact_param(config_space, param)
    return impact_params