import argparse
import random
from enumerates import Type
from parameter import Parameter
from configuration import Configuration
from acotsp import Scenario
from artificial1 import Artificial

## (1) parse command-line
parser = argparse.ArgumentParser(description='Generate data for artificial scenarios.')
parser.add_argument('-s','--scenario',type=str,default='artificial1',help='Name of artificial scenario.')
parser.add_argument('-n','--nsamples',type=int,default=1000,help='Number of samples.')
args = parser.parse_args()

NUM_CONFIGS = args.nsamples
SCENARIO_NAME = args.scenario

## (2) generate data
scenario = Artificial()
instances = scenario.get_instance_set()
configurations = []

for _ in range(NUM_CONFIGS):
    configurations.append(scenario.get_random_configuration())

file = open('./data/' + SCENARIO_NAME + '-rf.txt', 'w')
file2 = open('./data/' + SCENARIO_NAME + '-imp-rnd-rf.txt', 'w')
header = ''
for param in scenario.parameters:
    header += param.name + ' '
header += '.PERFORMANCE.'
file.write(header + '\n')
file2.write(header + '\n')
for config in configurations:
    line = ''
    for param in config.parameters:
        line += str(config.parameters[param] if config.parameters[param] is not None else 'NA') + ' '
    result = scenario.run(config)
    line += str(result)
    file.write(line + '\n')
    file2.write(line.replace('NA', str(random.random())) + '\n')
file2.close()
file.close()