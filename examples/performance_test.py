from sql_assurance.test.cases import PerformanceTestCase
from sql_assurance.test.cases import set_connector


class MyDummyConnectorTest(PerformanceTestCase):
    @set_connector(connection="dummy_test")
    def test_some_quer(self):
        self.assert_timing(
            "select * from everything",
            3,
            2
        )