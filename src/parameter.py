from enumerates import Type

AMOUNT = 3

class Parameter:
    def __init__(self, _name, _command, _type, _domain, _conditions = ''):
        self.name = _name
        self.command = _command
        self.type = _type
        self.domain = _domain
        self.conditions = _conditions
        self.values = self.__get_values()

    def __get_values(self):
        if self.type == Type.CATEGORICAL:
            return self.domain
        if self.type == Type.INTEGER:
            step = (self.domain[1] - self.domain[0]) / (AMOUNT - 2 + 1)
            return [int(round(self.domain[0] + (i * step), 0)) for i in range(0, AMOUNT)]
            #return [i for i in range(self.domain[0], self.domain[1] + 1)]
        if self.type == Type.REAL:
            step = (self.domain[1] - self.domain[0]) / (AMOUNT - 2 + 1)
            return [round(self.domain[0] + (i * step), 2) for i in range(0, AMOUNT)]

    def __str__(self):
        return 'Parameter: ' + self.name + ' (' + str(self.type) + ', ' + str(self.domain) + ', ' + ('no conditions' if self.conditions == '' else self.conditions) + ')'

    def __repr__(self):
        return self.__str__()