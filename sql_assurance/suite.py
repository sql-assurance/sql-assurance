class TestSuite(object):
    def __init__(self, tests=[]):
        self.__tests = tests
        self.__index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.__index >= len(self.__tests):
            raise StopIteration()

        test = self.__tests[self.__index]
        self.__index += 1

        return test