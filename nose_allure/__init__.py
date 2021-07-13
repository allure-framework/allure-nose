# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"

import os
import sys
import traceback
from types import ModuleType
from functools import wraps

import nose
from allure.constants import Status, Label
from nose.plugins.base import Plugin
from nose.plugins.attrib import AttributeSelector

from .utils import AllureWrapper, get_labels


def run_only_when_suite_exist(func):
    """
    Decorator to disable method if allure doesnt have any active suites.
    This is needed to avoid of IndexError that hides the real exception.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.allure.impl.stack:
            return func(self, *args, **kwargs)

    return wrapper


class Allure(Plugin):

    test_suite = False

    def options(self, parser, env):
        super(Allure, self).options(parser, env)

        parser.add_option('--logdir', dest='logdir')
        parser.add_option('--not-clear-logdir', dest='not_clear_logdir',
                          action='store_true', default=False)
        parser.add_option('--feature', dest='feature')
        parser.add_option('--story', dest='story')
        parser.add_option('--issue', dest='issue')
        parser.add_option('--severity', dest='severity')

    def configure(self, options, conf):
        super(Allure, self).configure(options, conf)
        self.options = options

        if options.logdir:
            logdir = os.path.normpath(os.path.abspath(os.path.expanduser(
                os.path.expandvars(options.logdir))))

            if not os.path.isdir(logdir):
                os.makedirs(logdir)
            else:
                # Need to provide an option to skip dir cleaning due to multiprocess
                # plugin usage can lead to logdir cleaning at the end of testing.
                # Unfortunately not possible to detect is it child process or parent.
                # Otherwise possible to clean logdir only in parent process always.
                if not options.not_clear_logdir:
                    for file_name in os.listdir(logdir):
                        file_path = os.path.join(logdir, file_name)
                        if os.path.isfile(file_path):
                            os.unlink(file_path)

            self.allure = nose.allure = AllureWrapper(logdir)

        for label in 'feature', 'story', 'issue', 'severity':
            if getattr(options, label, None):

                if not getattr(options, 'attr', None):
                    options.attr = []

                get_attr = lambda l: "%s_%s=%s" % \
                    (Label.DEFAULT, getattr(Label, label.upper()), l.strip())
                attrs = map(get_attr, getattr(options, label).split(','))

                options.attr.extend(attrs)

        if options.attr:
            for plugin in self.conf.plugins.plugins:
                if isinstance(plugin, AttributeSelector):
                    plugin.configure(options, conf)
                    break

    def begin(self):
        if not self.conf.options.logdir:
            raise LookupError('Should provide "--logdir" argument!')

    def startTest(self, test):
        if not self.test_suite:
            context_name = getattr(test.context, '__module__',
                                   test.context.__name__)
            self.allure.impl.start_suite(name=context_name,
                                         description=test.context.__doc__ or None)
            self.test_suite = True

        if hasattr(test.test, "test"):
            method = test.test.test
        else:
            method = getattr(test.test, test.test._testMethodName)

        hierarchy = ".".join(filter(None, test.address()[1:]))

        self.allure.impl.start_case(hierarchy, description=method.__doc__,
                                    labels=get_labels(method))

    @run_only_when_suite_exist
    def stopTest(self, test):
        # if we running in multiprocess mode we should trigger suite closing
        # each time when we exiting test
        if self.options.multiprocess_workers:
            self.allure.impl.stop_suite()
            self.test_suite = False

    @run_only_when_suite_exist
    def stopContext(self, context):
        # if we running not in multiprocess mode we should trigger suite
        # closing only when exiting context
        if not self.options.multiprocess_workers and self.test_suite and \
                isinstance(context, ModuleType):
            self.allure.impl.stop_suite()
            self.test_suite = False

    @run_only_when_suite_exist
    def addError(self, test, err):
        message, trace = self._parse_tb(err)
        self.allure.impl.stop_case(Status.BROKEN, message=message, trace=trace)

    @run_only_when_suite_exist
    def addFailure(self, test, err):
        message, trace = self._parse_tb(err)
        self.allure.impl.stop_case(Status.FAILED, message=message, trace=trace)

    @run_only_when_suite_exist
    def addSuccess(self, test):
        self.allure.impl.stop_case(Status.PASSED)

    @run_only_when_suite_exist
    def addSkip(self, test):
        self.allure.impl.stop_case(Status.CANCELED)

    def finalize(self, result):
        self.allure.impl.store_environment()

    @staticmethod
    def _parse_tb(trace):
        if type(trace[1]) is str:
            trace = sys.exc_info()

        message = ''.join(
            traceback.format_exception_only(trace[0], trace[1])).strip()
        trace = ''.join(traceback.format_exception(*trace)).strip()
        return message, trace
