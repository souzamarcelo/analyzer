from enumerates import Type
from parameter import Parameter
from configuration import Configuration
from functions import get_config_space
from functions import evaluate_config_space
from functions import globality
from functions import impact
import testcases

EPSILON = 0

def analyze(scenario):
    config_space = get_config_space(scenario)
    config_space = evaluate_config_space(scenario, config_space)
    res_globality = globality(scenario, config_space, EPSILON)
    res_impact = impact(scenario, config_space)
    #
    print(f'{scenario.name.upper()}:')
    print('=== Globality ===')
    for param in res_globality:
        print(f'{param}: G={res_globality[param][0]:.2f}  G\'={res_globality[param][1]:.2f}')
    print()
    print('===== Impact ====')
    for param in res_impact:
        print(f'{param}: I={res_impact[param][0]:.2f}  I\'={res_impact[param][1]:.2f}')
    print('\n')


scenario = testcases.TestCase1()
analyze(scenario)
scenario = testcases.TestCase2()
analyze(scenario)
scenario = testcases.TestCase2_1()
analyze(scenario)
scenario = testcases.TestCase2_2()
analyze(scenario)
scenario = testcases.TestCase2_3()
analyze(scenario)
scenario = testcases.TestCase3()
analyze(scenario)
scenario = testcases.TestCase4ab()
analyze(scenario)
scenario = testcases.TestCase4abcd()
analyze(scenario)
scenario = testcases.TestCase5()
analyze(scenario)
scenario = testcases.TestCase6()
analyze(scenario)