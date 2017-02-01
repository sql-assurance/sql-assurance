import time
import hashlib
import time

from numpy import mean
from datetime import timedelta
from functools import wraps

from sql_assurance.connectors.connection import ConnectionPoolBuilder
from sql_assurance.config import path_to_config_file


def set_connector(connection):
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            connection_pool = ConnectionPoolBuilder(
                path_to_config_file
            )

            self.__class__.test_name = f.__name__
            self.__class__.connector = connection_pool.get_connection(connection)

            return f(self, *args, **kwargs)

        return wrapped

    return wrapper


class SQLTestCase(object):
    def __init__(self):
        self._queries_executed = {}

        super(SQLTestCase, self).__init__()

    def _execute_query(self, query):
        raise NotImplementedError("This TestCase should implement the execute_query")

    def _get_query_hash(self, query):
        return hashlib.md5("{}.{}".format(query, str(time.time()))).hexdigest()

    def __del__(self):
        if self._queries_executed:
            pass


class PerformanceTestCase(SQLTestCase):
    def __init__(self):
        super(PerformanceTestCase, self).__init__()

    def _execute_query(self, query):
        data = self.connector.query(query)

        return self._get_query_hash(query), data

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
            query_hash, data = self._execute_query(query)
            end_time = time.time()

            results.append(
                timedelta(seconds=float(end_time - start_time)).total_seconds()
            )

        end_result = mean(results)

        test_passed = True
        if float(end_result) > float(mean_lower_than):
            test_passed = False

        # store results
        self._queries_executed[query_hash] = {
            "test_passed": test_passed,
            "execution_time": end_result,
            "expected_value": mean_lower_than,
            "query": query,
            "executed_at": time.time()
        }

        if not test_passed:
            raise Exception("Test {} failed, expected lower than {} and result was {}".format(
                self.test_name, mean_lower_than, end_result
            ))

        return True


class StatisticalHypothesisTest(SQLTestCase):
    def __init__(self):
        super(StatisticalHypothesisTest, self).__init__()
