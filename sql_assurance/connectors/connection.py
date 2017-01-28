import os
import yaml

from backends import *
from sql_assurance.connectors.backends import impala_driver


class ConnectionFactory(object):
    def __init__(self):
        self.__allowed_backends = [
            'impala', 'mysql', 'dummy'
        ]

    def get_connection(self, connection, config):
        if connection not in self.__allowed_backends:
            raise ValueError("{} driver is not supported".format(connection))

        if connection == "impala":
            return impala_driver.ImpalaConnector(
                host=config["host"],
                port=config["port"],
                database=config["database"]
            )
        elif connection == "dummy":
            return dummy_driver.DummyConnector(config)


class ConnectionPool(object):
    def __init__(self, config_path):
        self.__config = self._load_config(config_path)
        self.__connections = {}

    def get_connection(self, connection_id):
        if connection_id not in self.__config:
            raise ValueError(
                "Connection {} do not exists".format(connection_id)
            )

    @property
    def config(self):
        return self.__config

    def _load_config(self, config_path):
        if not os.path.exists(config_path):
            raise Exception("{} config file do not exists".format(config_path))

        with open(config_path, 'r') as config_buffer:
            config_yml = yaml.load(config_buffer.read())
        config_buffer.close()

        return config_yml
