from enumerates import Type
from parameter import Parameter
from configuration import Configuration
from scenario import Scenario

scenario = Scenario()
base_configs = []

instances = {}
for instance in scenario.get_instance_set():
    instances[instance] = (float('inf'), float('-inf'))

results = {}
for param in scenario.parameters:
    results[param] = {}
    for instance in instances:
        results[param][instance] = []

def analyze():
    print('Total base configurations: ' + str(len(base_configs)))
    print('Last base configuration: ' + str(base_configs[-1][0]) + ' = ' + str(base_configs[-1][1]))
    print('Parameter importance:')
    importance = []
    for param in scenario.parameters:
        sum_param = 0
        for instance in results[param]:
            if len(results[param][instance]) > 0:
                max_instance = instances[instance][1] - instances[instance][0]
                sum_param_instance = 0
                for result_instance in results[param][instance]:
                    sum_param_instance += result_instance / max_instance
                result_param_instance = sum_param_instance / len(results[param][instance])
                sum_param += result_param_instance
        result_param = sum_param / len(instances)
        importance.append((param, round(result_param, 4)))
    importance.sort(key = lambda x: x[1], reverse = True)
    counter = 0
    for item in importance:
        counter += 1
        print(str(counter) + '. ' + item[0].name + ': ' + str(item[1]))
    print('----------')

def update_instances(instance, new_result):
    best_instance = min(instances[instance][0], new_result)
    worst_instance = max(instances[instance][1], new_result)
    instances[instance] = (best_instance, worst_instance)

while True:
    configuration = scenario.get_random_configuration()
    for instance in instances:
        configuration_result = scenario.run(configuration, instance)
        update_instances(instance, configuration_result)
        base_configs.append((configuration, configuration_result))
        for param in scenario.parameters:
            if configuration.parameters[param] is None: continue
            worst_param = configuration_result
            best_param = configuration_result
            for value in param.values:
                if value == configuration.parameters[param]: continue
                children = configuration.children(param, value)
                best_children = float('inf')
                for child in children:
                    result = scenario.run(child, instance)
                    best_children = min(result, best_children)
                worst_param = max(best_children, worst_param)
                best_param = min(best_children, best_param)
                update_instances(instance, worst_param)
                update_instances(instance, best_param)
            results[param][instance].append(worst_param - best_param)
    analyze()