===============================
SQLAssurance (Under heavy development)
===============================

SQLAssurance is a programmer oriented SQL Testing framework. A full name for this kind of testing could be: **Scheduled xSQL Testing**.

This testing framework is able to work in a two different modes:

1. You can execute the sql-assurance script **like any other testing framework**, you will have as a result something like the image below this text: ![SQLAssurance](http://i.imgur.com/6DtPK9X.png)
2. You can **schedule your tests individually**, for instance, you want to execute specific query every night at 2am. This can be useful to track if your query and your data are behaving as expected.



Features
--------

This testing frameworks gives you out of the box drivers to connect to the following data sources:

- [x] Impala
- [ ] MySQL
- [ ] PostgreSQL
- [ ] MongoDB

For testing purposes we have created different Test Cases, at the moment we are supporting those:

- **PerformanceTestCase**: It tries to execute specific query as many times as you specified calculating at the end the mean, to succeed on this test the mean should be lower than the one provided on the expected value.

- **StatisticalHypothesisTestCase**: This test case helps you to assure the quality of your data, for instance, today I had 1000 new records on this table, does that makes sense comparing with the historical data you have?

- [x] PerformanceTestCase, basic assert_timing
- [ ] StatisticalHypothesisTestCase
- [ ] SchemaTestCase (but included in the main SQLTestCase)

## Examples

### PerformanceTestCase

```python
class DummyTest(PerformanceTestCase):
    @set_connector(connection='impala_staging')
    def test_collect_customers_for_us(self):
        self.assert_timing("select * from customers where country='US' limit 100", 3, 3)

    @set_connector(connection='impala_production')
    def test_joining_orders_and_customers(self):
        self.assert_timing("select * from orders left join customers on fk_customer = id_customer limit 10", 2, 1.2)

    @set_connector(connection='mysql_connection')
    def test_grouping_orders_by_week(self):
        self.assert_timing('select * from orders group by week', 4, 0.2)
```
