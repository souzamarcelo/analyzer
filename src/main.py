from enumerates import Type
from parameter import Parameter
from configuration import Configuration
from functions import get_config_space
from functions import evaluate_config_space
from testcases import TestCase1

# ========== TestCase 1
scenario = TestCase1()
config_space = get_config_space(scenario)
config_space = evaluate_config_space(scenario, config_space)