from time import sleep


class DummyConnector(object):
    def __init__(self, config):
        self.__config = config

    def query(self, sql_statement):
        sleep(1)
        return []

    @property
    def config(self):
        return self.__config
