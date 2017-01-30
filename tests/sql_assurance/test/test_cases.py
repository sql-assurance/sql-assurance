import unittest

from sql_assurance.test.cases import PerformanceTest
from sql_assurance.test.cases import set_connector


class DummyTest(PerformanceTest):
    @set_connector(connection='dummy_test')
    def test_something_weird(self, query, attempts=3, median_lower_than=0.9):
        self.assert_timing(query)


class TestPerformanceTest(unittest.TestCase):
    def test_assert_timing(self):
        test = DummyTest()

        with self.assertRaises(Exception) as context:
            test.test_something_weird("test")

        self.assertTrue("Test test_something_weird failed" in context.exception)
