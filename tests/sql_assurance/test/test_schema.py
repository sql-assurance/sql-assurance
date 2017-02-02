import unittest

from sql_assurance.test.schema import SchemaCheckerFactory
from sql_assurance.test.schema import AssertSchema
from sql_assurance.test.schema import AvroSchemaChecker


class SchemaCheckerFactoryTest(unittest.TestCase):
    def test_get_file_extension(self):
        file_path = "/dir/path/something/schema.avro"

        self.assertEqual(
            'avro', SchemaCheckerFactory._get_extension_from_path(file_path)

        )


class AssertSchemaTest(unittest.TestCase):
    def test_it_fails_with_wrong_schema_path(self):
        with self.assertRaises(Exception) as context:
            AssertSchema.assert_schema([], 'to some path')

        self.assertTrue(
            "Schema path to some path not found" in context.exception
        )

    def test_it_returns_proper_schema_checker(self):
        self.assertIsInstance(
            SchemaCheckerFactory.get_schema_checker('/path/file.avsc'),
            AvroSchemaChecker
        )

    def test_with_unsupported_schema_checker(self):
        with self.assertRaises(ValueError) as context:
            SchemaCheckerFactory.get_schema_checker('file.unsupported')

        self.assertTrue(
            'Checker unsupported not supported' in context.exception
        )


class AvroSchemaCheckerTest(unittest.TestCase):
    def test_with_valid_schema(self):
        data = {
            "name": "My Name",
            "favorite_number": 10,
            "favorite_color": "red"
        }

        checker = AvroSchemaChecker()
        checker.check_schema(data, 'fixtures/test.avsc')