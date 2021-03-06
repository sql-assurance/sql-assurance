import os
import sys
import fnmatch

from test.cases import SQLTestCase
from suite import TestSuite


class Finder(object):
    FILE_PATTERN = 'test*.py'

    def __init__(self):
        pass

    def find(self, path):
        test_suite = self._find_tests(path)

        return test_suite

    def _find_tests(self, start_dir):
        files = self._load_files(start_dir)
        tests = []

        for file_ in files:
            module_path = self._get_name_from_path(file_)
            module = self._get_module_from_name(module_path)
            tests += self._get_tests_from_module(module)

        return TestSuite(tests)

    def _load_files(self, start_dir):
        file_list = []

        for root, dirnames, filenames in os.walk(start_dir):
            for filename in fnmatch.filter(filenames, self.FILE_PATTERN):
                file_list.append(os.path.join(root, filename))

        return file_list

    @staticmethod
    def _get_tests_from_module(module):
        tests = []

        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, SQLTestCase):
                methods = [method for method in dir(obj()) if method[0:5] == "test_"]
                for method in methods:
                    tests.append(getattr(obj(), method))

        return tests

    @staticmethod
    def _get_module_from_name(name):
        __import__(name)
        return sys.modules[name]

    @staticmethod
    def _get_name_from_path(path):
        path = os.path.splitext(os.path.normpath(path))[0]

        assert not os.path.isabs(path), "Path must be within the project"
        assert not path.startswith('..'), "Path must be within the project"

        name = path.replace(os.path.sep, '.')
        return name
