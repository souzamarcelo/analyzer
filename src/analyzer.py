import sys
from enumerates import Type
from parameter import Parameter
from configuration import Configuration
from acotsp import Scenario
from artificial0 import Artificial0
from artificial1 import Artificial1
from artificial2 import Artificial2

scenario = None
SCENARIO_NAME = sys.argv[1]
if SCENARIO_NAME == 'artificial0':
    scenario = Artificial0()
if SCENARIO_NAME == 'artificial1':
    scenario = Artificial1()
if SCENARIO_NAME == 'artificial2':
    scenario = Artificial2()

base_configs = []

def best(value1, value2):
    if scenario.maximization: return max(value1, value2)
    else: return min(value1, value2 )

def worst(value1, value2):
    if scenario.maximization: return min(value1, value2)
    else: return max(value1, value2)

def difference(best, worst):
    if scenario.maximization: return best - worst
    else: return worst - best

instances = {}
for instance in scenario.get_instance_set():
    instances[instance] = (worst(float('-inf'), float('inf')), best(float('-inf'), float('inf')))

results = {}
for param in scenario.parameters:
    results[param] = {}
    for instance in instances:
        results[param][instance] = []

def analyze():
    print('Total base configurations: ' + str(len(base_configs)), flush = True)
    print('Last base configuration: ' + str(base_configs[-1][0]) + ' = ' + str(base_configs[-1][1]), flush = True)
    print('Parameter importance:', flush = True)
    importance = []
    for param in scenario.parameters:
        sum_param = 0
        for instance in results[param]:
            if len(results[param][instance]) > 0:
                diff_instance = max(difference(instances[instance][0], instances[instance][1]), 1)
                #if param == scenario.parameters[0]: print('DIFF INSTANCE: ' + str(diff_instance))
                sum_param_instance = 0
                for result_instance in results[param][instance]:
                    #if param == scenario.parameters[0]: print('A result: ' + str(result_instance / diff_instance))
                    sum_param_instance += result_instance / diff_instance
                result_param_instance = sum_param_instance / len(results[param][instance])
                #if param == scenario.parameters[0]: print('Result on instance: ' + str(result_param_instance))
                sum_param += result_param_instance
        result_param = sum_param / len(instances)
        #if param == scenario.parameters[0]: print('Result PARAM: ' + str(result_param))
        importance.append((param, round(result_param, 4)))
    importance.sort(key = lambda x: x[1], reverse = True)
    counter = 0
    for item in importance:
        counter += 1
        print(str(counter) + '. ' + item[0].name + ': ' + str(item[1]), flush = True)
    print('----------')

def update_instances(instance, new_result):
    best_instance = best(instances[instance][0], new_result)
    worst_instance = worst(instances[instance][1], new_result)
    instances[instance] = (best_instance, worst_instance)

configurations = []
file_configs = open('./data/configs-' + SCENARIO_NAME + '.txt', 'r')
for line in file_configs:
    line = line.replace('\n', '')
    content = line.split(',')
    values = [float(value) if value != 'None' else None for value in content]
    configurations.append(Configuration(scenario.parameters, values))

#while True:
#    configuration = scenario.get_random_configuration()
for configuration in configurations:
    #print('Base configuration: ' + str(configuration))
    for instance in instances:
        configuration_result = scenario.run(configuration, instance)
        #print('Result: ' + str(configuration_result))
        update_instances(instance, configuration_result)
        base_configs.append((configuration, configuration_result))
        for param in scenario.parameters:
            #print('Parameter: ' + str(param))
            if configuration.parameters[param] is None: continue
            worst_param = configuration_result
            best_param = configuration_result
            #print(param.values)
            for value in param.values:
                if value == configuration.parameters[param]: continue
                children = configuration.children(param, value)
                #print('Value: ' + str(value))
                #print('Children: ' + str(children))
                best_children = worst(float('-inf'),float('inf'))
                for child in children:
                    result = scenario.run(child, instance)
                    #print('Child: ' + str(child))
                    #print('Result: ' + str(result))
                    #print('---')
                    best_children = best(result, best_children)
                worst_param = worst(best_children, worst_param)
                best_param = best(best_children, best_param)
                #print('Worst: ' + str(worst_param))
                #print('Best: ' + str(best_param))
                update_instances(instance, worst_param)
                update_instances(instance, best_param)
            #exit()
            results[param][instance].append(difference(best_param, worst_param))
            #print('Parameter: ' + str(param))
            #print('Worst: ' + str(worst_param))
            #print('Best: ' + str(best_param))
            #print('Adding: ' + str(difference(best_param, worst_param)))
            #print('=====')
    analyze()