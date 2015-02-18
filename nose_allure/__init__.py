# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"

import traceback
from types import ModuleType

import nose
from allure.constants import Status, Label
from nose.plugins.base import Plugin
from nose.plugins.attrib import AttributeSelector

from .utils import AllureWrapper, get_labels


class Allure(Plugin):

    def options(self, parser, env):
        super(Allure, self).options(parser, env)

        parser.add_option('--logdir', dest='logdir')
        parser.add_option('--feature', dest='feature')
        parser.add_option('--story', dest='story')
        parser.add_option('--issue', dest='issue')
        parser.add_option('--severity', dest='severity')

    def configure(self, options, conf):
        super(Allure, self).configure(options, conf)

        if options.logdir:
            self.allure = nose.allure = AllureWrapper(options.logdir)

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

    def startContext(self, context):
        if isinstance(context, ModuleType):
            self.allure.impl.start_suite(name=context.__name__,
                                         description=context.__doc__)

    def stopContext(self, context):
        if isinstance(context, ModuleType):
            self.allure.impl.stop_suite()

    def startTest(self, test):
        self.allure.impl.start_case(test, description=test.test.test.__doc__,
                                    labels=get_labels(test))

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
