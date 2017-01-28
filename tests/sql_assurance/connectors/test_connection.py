import unittest
from thrift.transport.TTransport import TTransportException

from sql_assurance.connectors.connection import ConnectionPool
from sql_assurance.connectors.connection import ConnectionFactory


class TestConnectionFactory(unittest.TestCase):
    def setUp(self):
        self.connection_factory = ConnectionFactory()

    def test_with_not_supported_driver(self):
        with self.assertRaises(ValueError) as context:
            self.connection_factory.get_connection('wordpress', {})

        self.assertTrue(
            'wordpress driver is not supported' in context.exception
        )

    def test_with_an_existing_driver(self):
        connection = self.connection_factory.get_connection('dummy',
            {"host": "test", "port": 1234, "database": "test"}
        )

        config = connection.config
        self.assertEqual(
            {'host': 'test', 'port': 1234, 'database': 'test'},
            config
        )


class TestConnectionPool(unittest.TestCase):
    def setUp(self):
        self.connection = ConnectionPool('dummy_config.yml')

    def test_get_dummy_connection(self):
        config = self.connection.config

        expected_output = {
            'imapala_test':
                {
                    'connector': 'impala',
                    'config': {'host': 'test', 'port': 'test', 'database': 'test'}
                }
        }

        self.assertEqual(expected_output, config)

    def test_get_connection_do_not_exists(self):
        with self.assertRaises(ValueError) as context:
            self.connection.get_connection('something_broken')

        self.assertTrue(
            'Connection something_broken do not exists' in context.exception
        )
