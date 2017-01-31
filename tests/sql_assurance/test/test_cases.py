import unittest

from sql_assurance.test.cases import PerformanceTestCase
from sql_assurance.test.cases import set_connector


class DummyTest(PerformanceTestCase):
    @set_connector(connection='dummy_test')
    def test_something_weird(cls, query, attempts=3, mean_lower_than=0.9):
        cls.assert_timing(query, attempts, mean_lower_than)


class TestPerformanceTest(unittest.TestCase):
    def test_assert_timing_failed(self):
        test = DummyTest()

        with self.assertRaises(Exception) as context:
            test.test_something_weird("test")

        self.assertTrue("Test test_something_weird failed" in context.exception[0][0:32])

    def test_assert_timing_success(self):
        test = DummyTest()

        # Run it 2 times and mean should be lower than 2
        test.test_something_weird("query", 2, 2)
