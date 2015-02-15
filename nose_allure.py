# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"

import traceback

import nose
from allure.common import AllureImpl
from allure.constants import Status, AttachmentType
from allure.pytest_plugin import LazyInitStepContext
from nose.plugins.base import Plugin


class AllureWrapper(object):

    def __init__(self, logdir):
        self.impl = AllureImpl(logdir)

    get_listener = lambda self: self.impl  # compatibility with pytest_plugin

    def attach(self, name, contents, type=AttachmentType.TEXT):
        self.impl.attach(name, contents, type)

    def step(self, title):
        """
        A contextmanager/decorator for steps.

        Usage examples::

          import nose

          def test_foo():
             with nose.allure.step('mystep'):
                 assert False

          @nose.allure.step('make test data')
          def make_test_data_bar():
              raise ValueError('No data today')

          def test_bar():
              assert make_test_data_bar()

          @nose.allure.step
          def make_test_data_baz():
              raise ValueError('No data today')

          def test_baz():
              assert make_test_data_baz()
        """
        if callable(title):
            return LazyInitStepContext(self, title.__name__)(title)
        else:
            return LazyInitStepContext(self, title)

    def environment(self, **env_dict):
        self.impl.environment.update(env_dict)


class Allure(Plugin):

    def options(self, parser, env):
        super(Allure, self).options(parser, env)
        parser.add_option('--logdir', dest='logdir')

    def configure(self, options, conf):
        super(Allure, self).configure(options, conf)
        if options.logdir:
            self.allure = nose.allure = AllureWrapper(options.logdir)

    def startContext(self, context):
        self.allure.impl.start_suite(name=context.__name__)

    def stopContext(self, context):
        self.allure.impl.stop_suite()

    def startTest(self, test):
        self.allure.impl.start_case(test)

    def addError(self, test, err):
        message, trace = self._parse_tb(err)
        self.allure.impl.stop_case(Status.BROKEN, message=message, trace=trace)

    def addFailure(self, test, err):
        message, trace = self._parse_tb(err)
        self.allure.impl.stop_case(Status.FAILED, message=message, trace=trace)

    def addSuccess(self, test):
        self.allure.impl.stop_case(Status.PASSED)

    def addSkip(self, test):
        self.allure.impl.stop_case(Status.CANCELED)

    def finalize(self, result):
        self.allure.impl.store_environment()

    @staticmethod
    def _parse_tb(trace):
        message = ''.join(
            traceback.format_exception_only(trace[0], trace[1])).strip()
        trace = ''.join(traceback.format_exception(*trace)).strip()
        return message, trace
