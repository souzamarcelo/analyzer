from enumerates import Type
from math import floor
from math import ceil

STEP = 100

class Parameter:
    def __init__(self, _name, _command, _type, _domain, _conditions = ''):
        self.name = _name
        self.command = _command
        self.type = _type
        self.domain = _domain
        self.conditions = _conditions

    def get_values(self):
        if self.type == Type.CATEGORICAL:
            return self.domain
        if self.type == Type.INTEGER:
            return [i for i in range(self.domain[0], self.domain[1] + 1)]
        if self.type == Type.REAL:
            return [r / STEP for r in range(floor(self.domain[0]), ceil(self.domain[1]) * int(STEP) + 1, 1) if (r / STEP) >= self.domain[0] and (r / STEP) <= self.domain[1]]