# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"

from .utils import launch, report_for, environment_for


def test_report_one_test():
    test_suite = """
def test_dummy():
    pass
"""

    reports = launch(test_suite)

    assert len(reports) == 1


def test_report_test_present():
    test_name = 'test_dummy'
    test_suite = """
def %s():
    pass
    """ % test_name

    report = report_for(test_suite)

    assert report.find('.//test-case/name').text.split('.')[-1] == test_name


def test_unittest():
    test_class = 'Testing'
    test_name = 'test_dummy'
    test_suite = """
import unittest

class %s(unittest.TestCase):
    def %s(self):
        self.assertTrue(True)
    """ % (test_class, test_name)

    report = report_for(test_suite)

    assert report.find('.//test-case/name').text.split('.')[-1] == test_name
    assert report.find('.//test-case/name').text.split('.')[-2] == test_class


def test_report_step_context():
    test_step = "check"
    test_suite = """
import nose

def test_dummy():
    with nose.allure.step("%s"):
        assert True
    """ % test_step

    report = report_for(test_suite)

    assert report.find('.//step/name').text == test_step


def test_report_step_decorator():
    test_step = "check"
    test_suite = """
import nose

@nose.allure.step("%s")
def dummy():
    pass

def test_dummy():
    dummy()
    """ % test_step

    report = report_for(test_suite)

    assert report.find('.//step/name').text == test_step


def test_report_attach():
    attach_name = "my attach"
    test_suite = """
import nose

def test_dummy():
    nose.allure.attach("%s", "hello world")
    """ % attach_name

    report = report_for(test_suite)

    assert report.findall('.//attachment[@title="%s"]' % attach_name)


def test_report_environment():
    env_name = "my_var"
    env_value = "my val"
    test_suite = """
import nose

def test_dummy():
    nose.allure.environment(%s="%s")
    """ % (env_name, env_value)

    environment = environment_for(test_suite)

    assert environment.find('.//key').text == env_name
    assert environment.find('.//value').text == env_value


def test_report_one_failed_test():
    error_message = "Invalid test"
    test_suite = """
import nose

def test_failed():
    with nose.allure.step("check"):
        assert False, "%s"
    """ % error_message

    report = report_for(test_suite)
    assert error_message in report.find('.//test-case/failure/message').text


def test_report_two_tests():
    test_suite = """
def test_passed():
    assert True

def test_failed():
    assert False
    """

    report = report_for(test_suite)

    assert len(report.findall('.//test-case/name')) == 2


def test_report_two_modules():
    test_suite = """
def test_passed():
    pass
--
def test_passed():
    pass
    """

    results = launch(test_suite)

    assert len(results) == 2


def test_report_class():
    class_name = 'TestDummy'
    test_suite = """
class %s(object):
    def test_passed(self):
        pass
    """ % class_name

    report = report_for(test_suite)

    assert class_name in report.find('.//test-case/name').text


def test_report_function_and_class():
    class_name = 'TestDummy'
    test_suite = """
def test_passed():
    pass

class %s(object):
    def test_passed(self):
        pass
    """ % class_name

    report = report_for(test_suite)

    assert len(report.findall('.//test-case/name')) == 2


def test_module_description():
    description = "I'm module!"
    test_suite = '''
"""%s"""
def test_dummy():
    pass
    ''' % description

    report = report_for(test_suite)

    assert report.find('.//description').text == description


def test_function_description():
    description = "I'm function!"
    test_suite = '''
def test_dummy():
    """%s"""
    ''' % description

    report = report_for(test_suite)

    assert report.find('.//test-case/description').text == description


def test_severity():
    severity = "very hard"
    test_suite = """
import nose

@nose.allure.severity("%s")
def test_dummy():
    pass
    """ % severity

    report = report_for(test_suite, argv=['--severity=%s' % severity])

    assert report.find(".//test-case//label[@name='severity']").attrib['value'] == severity


def test_issue():
    issue = "http://tracker.local/bugs/999"
    test_suite = """
import nose

@nose.allure.issue("%s")
def test_dummy():
    pass
    """ % issue

    report = report_for(test_suite, argv=['--issue=%s' % issue])

    assert report.find(".//test-case//label[@name='issue']").attrib['value'] == issue


def test_feature():
    feature = "my feature"
    test_suite = """
import nose

@nose.allure.feature("%s")
def test_dummy():
    pass
    """ % feature

    report = report_for(test_suite, argv=['--feature=%s' % feature])

    assert report.find(".//test-case//label[@name='feature']").attrib['value'] == feature


def test_story():
    story = "love story"
    test_suite = """
import nose

@nose.allure.story("%s")
def test_dummy():
    pass
    """ % story

    report = report_for(test_suite, argv=['--story=%s' % story])

    assert report.find(".//test-case//label[@name='story']").attrib['value'] == story


def test_story_and_feature():
    story = "Love story"
    feature = "My feature"
    test_suite = """
import nose

@nose.allure.story("%s")
def test_1():
    pass

@nose.allure.feature("%s")
def test_2():
    pass
    """ % (story, feature)

    report = report_for(test_suite, argv=['--story=%s' % story, '--feature=%s' % feature])

    assert len(report.findall(".//test-case/name")) == 2


def test_several_features():
    feature1 = "My feature"
    feature2 = "Your feature"
    test_suite = """
import nose

@nose.allure.feature("%s")
def test_1():
    pass

@nose.allure.feature("%s")
def test_2():
    pass
    """ % (feature1, feature2)

    report = report_for(test_suite, argv=['--feature=%s, %s' % (feature1, feature2)])

    assert len(report.findall(".//test-case/name")) == 2


def test_feature_and_severity():
    feature = "login"
    severity = "easy"
    test_suite = """
import nose

@nose.allure.severity("%s")
@nose.allure.feature("%s")
def test_dummy():
    pass

def test_another():
    pass
    """ % (severity, feature)

    report = report_for(test_suite, argv=['--feature=%s' % feature, '--severity=%s' % severity])

    assert len(report.findall(".//test-case/name")) == 1
