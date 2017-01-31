import time

from numpy import mean
from datetime import timedelta
from functools import wraps

from sql_assurance.connectors.connection import ConnectionPool
from sql_assurance.config import path_to_config_file


def set_connector(connection):
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            connection_pool = ConnectionPool(
                path_to_config_file
            )

            self.__class__.test_name = f.__name__
            self.__class__.connector = connection_pool.get_connection(connection)

            return f(self, *args, **kwargs)

        return wrapped

    return wrapper


class TestCase(object):
    def __init__(self):
        pass


class PerformanceTestCase(TestCase):
    def __init__(self):
        super(PerformanceTestCase, self).__init__()

    def assert_timing(self, query, attempts=3, mean_lower_than=1.5):
        """
        :param query: Which query we need to execute to a given connector
        :param attempts: Number of times that query should be executed
        :param mean_lower_than: Total mean should be lower than this value
        :return: True / Raise exception
        """

        results = []
        for i in xrange(0, attempts):
            start_time = time.time()
            self.connector.query(query)
            end_time = time.time()

            results.append(
                timedelta(seconds=float(end_time - start_time)).total_seconds()
            )

        end_result = mean(results)

        if float(end_result) > float(mean_lower_than):
            raise Exception("Test {} failed, expected lower than {} and result was {}".format(
                self.test_name, mean_lower_than, end_result
            ))

        return True


class StatisticalHypothesisTest(TestCase):
    def __init__(self):
        super(StatisticalHypothesisTest, self).__init__()
