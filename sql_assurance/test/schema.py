import os
import avro.schema

from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter



class SchemaChecker(object):
    def check_schema(self, data, schema_path):
        raise NotImplementedError("This method should be implemented")


class AvroSchemaChecker(SchemaChecker):
    def check_schema(self, data, schema_path):
        schema = avro.schema.Parse(
            open(schema_path, "rb").read().decode("utf-8")
        )

        writer = DataFileWriter(
            open('_test.avro', "wb"), DatumWriter(), schema
        )

        writer.append(data)
        writer.close()


class SchemaCheckerFactory(object):
    @staticmethod
    def get_schema_checker(schema_path=None):
        file_extension = SchemaCheckerFactory._get_extension_from_path(schema_path)

        if file_extension == 'avsc':
            return AvroSchemaChecker()

        raise ValueError("Checker {} not supported".format(file_extension))

    @staticmethod
    def _get_extension_from_path(path):
        return os.path.splitext(path)[1].replace('.', "")


class AssertSchema(object):
    @staticmethod
    def assert_schema(data, schema_path):
        if not os.path.exists(schema_path):
            raise ValueError("Schema path {} not found".format(schema_path))

        checker = SchemaCheckerFactory.get_schema_checker(schema_path)

        return checker.check_schema(data, schema_path)
