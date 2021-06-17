class Configuration:
    def __init__(self, parameters, values = None):
        self.map = {}
        for index in range(len(parameters)):
            self.map[parameters[index]] = None if values is None else values[index]