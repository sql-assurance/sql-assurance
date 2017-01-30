import time

from numpy import mean
from datetime import timedelta
from functools import wraps

from sql_assurance.connectors.connection import ConnectionPool


def set_connector(connection):
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            # TODO: Find a way to get this global ConnectionPool
            connection_pool = ConnectionPool(
                '/Users/ssola/Workspace/sql-assurance/resources/config/connections.yml'
            )

            self.__class__.test_name = f.__name__
            self.__class__.connector = connection_pool.get_connection(connection)

            return f(self, *args, **kwargs)

        return wrapped

    return wrapper


class PerformanceTest(object):
    def __init__(self):
        # How to pass the ConnectionPool?
        pass

    def assert_timing(self, query, attempts=3, median_lower_than=1.5):
        results = []
        for i in xrange(0, attempts):
            start_time = time.time()
            self.connector.query(query)
            end_time = time.time()

            results.append(
                timedelta(seconds=float(end_time - start_time)).total_seconds()
            )

            end_result = mean(results)

            if not float(end_result) > float(median_lower_than):
                raise Exception("Test {} failed".format(self.test_name))

            return True

