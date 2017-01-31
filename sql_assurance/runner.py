from termcolor import colored


class Runner(object):
    def __init__(self):
        self.__errors = []

    @property
    def errors(self):
        return self.__errors

    def run(self, test_suite):
        for test in test_suite:
            self.__executor(test)

    def __executor(self, test):
        module_ = test.__module__
        class_ = test.im_class.__name__
        method_ = test.__name__

        full_test_name = "{}.{}.{}".format(
            module_, class_, method_
        )
        print "Testing {}".format(
            full_test_name
        ),

        try:
            result_ = test()
            print colored("\t\tSuccess\r\n", "green")
        except Exception, e:
            print colored("\t\tFailed\r\n", "red")
            print "{}\r\n".format(e)
            self.__errors.append((full_test_name, e))

        return True
