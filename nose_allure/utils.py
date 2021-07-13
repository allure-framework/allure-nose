# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"

from allure.common import AllureImpl
from allure.constants import AttachmentType, Label, Severity
from allure.pytest_plugin import LazyInitStepContext
from allure.structure import TestLabel
from nose.plugins.attrib import attr


def get_labels(test):

    def get_markers(item, name):
        markers = []

        for prop in dir(item):
            if prop.startswith(Label.DEFAULT):
                key = prop.split('_')[-1]
                value = getattr(item, prop)
                markers.append((key, value))

        return markers

    labels = []
    label_markers = get_markers(test, Label.DEFAULT)
    for name, value in label_markers:
        labels.append(TestLabel(name=name, value=value))
    labels.append(TestLabel(name=Label.FRAMEWORK, value="nose"))
    labels.append(TestLabel(name=Label.LANGUAGE, value="python"))

    return labels


class Allure(AllureImpl):
    """By defaul AllureImpl clears logdir with instantiation. Using nosetests
    with key --processes=<n> can lead to cleaning of logdir at the end.
    """

    def __init__(self, logdir):
        self.logdir = logdir
        self.stack = []
        self.testsuite = None
        self.environment = {}


class AllureWrapper(object):

    def __init__(self, logdir):
        self.impl = Allure(logdir)

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

    def label(self, name, value):
        return attr(**{'%s_%s' % (Label.DEFAULT, name): value})

    def severity(self, severity):
        return self.label(Label.SEVERITY, severity)

    def feature(self, feature):
        return self.label(Label.FEATURE, feature)

    def story(self, story):
        return self.label(Label.STORY, story)

    def issue(self, issue):
        return self.label(Label.ISSUE, issue)

    def environment(self, **env_dict):
        self.impl.environment.update(env_dict)

    @property
    def severity_level(self):
        return Severity
