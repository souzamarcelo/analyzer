import argparse
import random
from enumerates import Type
from parameter import Parameter
from configuration import Configuration
from acotsp import Scenario
from artificial0 import Artificial0
from artificial1 import Artificial1
from artificial2 import Artificial2

## (1) parse command-line
parser = argparse.ArgumentParser(description='Generate data for artificial scenarios.')
parser.add_argument('-s','--scenario',type=str,default='artificial1',help='Name of artificial scenario.')
parser.add_argument('-n','--nsamples',type=int,default=1000,help='Number of samples.')
parser.add_argument('-p','--performance',type=str,default='raw',help='Performance measure: raw, norm.')
args = parser.parse_args()

NUM_CONFIGS = args.nsamples
SCENARIO_NAME = args.scenario
PERFORMANCE = args.performance

## (2) generate data
scenario = None
if SCENARIO_NAME == 'artificial0':
    scenario = Artificial0()
if SCENARIO_NAME == 'artificial1':
    scenario = Artificial1()
if SCENARIO_NAME == 'artificial2':
    scenario = Artificial2()
instances = scenario.get_instance_set()
configurations = []
results = []
for _ in range(NUM_CONFIGS):
    config = scenario.get_random_configuration()
    configurations.append(config)
    results.append(scenario.run(config))

if PERFORMANCE == 'norm':
    rmax = max(results)
    rmin = min(results)
    norm_results = []
    for result in results:
        norm_results.append((result - rmin) / (rmax - rmin))
    results = norm_results

file_fanova_features = open('./data/' + SCENARIO_NAME + '-' + PERFORMANCE + '-mid-' + str(NUM_CONFIGS) + '-features.csv', 'w')
file_fanova_response = open('./data/' + SCENARIO_NAME + '-' + PERFORMANCE + '-mid-' + str(NUM_CONFIGS) + '-response.csv', 'w')
file_rf = open('./data/' + SCENARIO_NAME + '-' + PERFORMANCE + '-random-' + str(NUM_CONFIGS) + '-rf.txt', 'w')
file_configs = open('./data/configs-' + SCENARIO_NAME + '.txt', 'w')

header = ''
for param in scenario.parameters:
    header += param.name + ','
header_fanova = header[:-1]
header_rf = header_fanova.replace(',', ' ') + ' .PERFORMANCE.'

file_fanova_features.write(header_fanova + '\n')
file_rf.write(header_rf + '\n')

for config in configurations:
    result = results[configurations.index(config)]
    config_fanova = ''
    config_rf = ''
    file_configs.write(str(config) + '\n')
    for param in config.parameters:
        config_fanova += str(config.parameters[param] if config.parameters[param] is not None else '0.5') + ','
        config_rf += str(config.parameters[param] if config.parameters[param] is not None else random.random()) + ' '
    config_fanova = config_fanova[:-1]
    file_fanova_features.write(config_fanova + '\n')
    file_fanova_response.write(str(result) + '\n')
    config_rf += str(result)
    file_rf.write(config_rf + '\n')
file_fanova_features.close()
file_fanova_response.close()
file_rf.close()
file_configs.close()