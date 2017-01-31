import os

from argparse import ArgumentParser
from finder import Finder
from termcolor import colored



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

        self.__finder.find(args.tests)

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
