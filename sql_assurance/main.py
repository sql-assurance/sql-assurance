import os

from argparse import ArgumentParser
from finder import Finder
from termcolor import colored
from runner import Runner
from config import settings



_LOGO = """
            .__
  ___________|  |           _____    ______ ________ ______________    ____   ____  ____
 /  ___/ ____/  |    ______ \__  \  /  ___//  ___/  |  \_  __ \__  \  /    \_/ ___\/ __ \\
 \___ < <_|  |  |__ /_____/  / __ \_\___ \ \___ \|  |  /|  | \// __ \|   |  \  \__\  ___/
/____  >__   |____/         (____  /____  >____  >____/ |__|  (____  /___|  /\___  >___  >
     \/   |__|                   \/     \/     \/                  \/     \/     \/    \/
    """


class SQLAssurance(object):
    def __init__(self):
        self.__finder = Finder()
        self.__runner = Runner()

    def run(self):
        print _LOGO
        args = self._parse_args()

        if not os.path.exists(args.path):
            print colored(
                'Error: {} file do not exists'.format(args.path),
                'red'
            )
            exit(-1)

        if not os.path.exists(args.tests):
            raise ValueError("Tests not found".format(
                args.tests
            ))

        # Find the test suite we need to execute
        test_suite = self.__finder.find(args.tests)

        # Run the test suite
        self.__runner.run(test_suite)


    @staticmethod
    def _parse_args():
        arg_parser = ArgumentParser()

        arg_parser.add_argument(
            '-p', '--path', dest='path', required=True,
            help='Define where the configuration file is located'
        )

        arg_parser.add_argument(
            '-t', '--tests', dest='tests', required=True,
            help='Define where to locate the tests'
        )

        return arg_parser.parse_args()
