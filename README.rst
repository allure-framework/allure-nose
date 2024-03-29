Deprecated
===================

Please follow https://github.com/allure-framework/allure-python


Allure Nose Adaptor
===================

.. image:: https://travis-ci.org/allure-framework/allure-nose-adaptor.svg?branch=master
        :alt: Build Status
        :target: https://travis-ci.org/allure-framework/allure-nose-adaptor/
.. image:: https://pypip.in/v/nose-allure-plugin/badge.png
        :alt: Release Status
        :target: https://pypi.python.org/pypi/nose-allure-plugin
.. image:: https://pypip.in/d/nose-allure-plugin/badge.png
        :alt: Downloads
        :target: https://pypi.python.org/pypi/nose-allure-plugin

It is a port of `pytest-allure-adaptor <https://github.com/allure-framework/allure-python>`_ for `nose framework <https://github.com/nose-devs/nose>`_.

Usage
=====

.. code:: bash

 nosetests --with-allure --logdir=/path/to/put/results
 nosetests --with-allure --logdir=/path/to/put/results --not-clear-logdir

Option "--not-clear-logdir" is useful with option "--processes" to prevent cleaning of logdr at the end of testing.

Supported features
==================

Attachment
----------

To attach some content to test report:

.. code:: python

 import nose
 
 def test_foo():
     nose.allure.attach('my attach', 'Hello, World')


Step
----

To divide a test into steps:

.. code:: python

 import nose

 def test_foo():
     with nose.allure.step('step one'):
         # do stuff

     with nose.allure.step('step two'):
         # do more stuff

Can also be used as decorators. By default step name is generated from method name:

.. code:: python

 import nose

 @nose.allure.step
 def make_test_data_foo():
     # do stuff

 def test_foo():
     assert make_some_data_foo() is not None

 @nose.allure.step('make_some_data_foo')
 def make_some_data_bar():
     # do another stuff

 def test_bar():
     assert make_some_data_bar() is not None

Environment
-----------

You can provide test `environment parameters <https://github.com/allure-framework/allure-core/wiki/Environment>`_ such as report name, browser or test server address to allure test report.

.. code:: python

 import nose

 def test_dummy():
     nose.allure.environment(report='Allure report', browser=u'Firefox')

Severity
--------

Any test, class or module can be marked with different severity:

.. code:: python

 import nose

 class TestBar(object):

     @nose.allure.severity(nose.allure.severity_level.CRITICAL)
     def test_bar(self):
         pass

 # custom severity
 @nose.allure.severity("hard")
 def test_bar(self):
     pass

To run tests with concrete priority:

.. code:: bash

 nosetests my_tests/ --with-allure --logdir=tmp --severity="critical, hard"


Issue
-----

Issues can be set for test.

.. code:: python

 import nose

 @nose.allure.issue('http://jira.lan/browse/ISSUE-1')
 def test_foo():
     assert False

Features & Stories
------------------

Feature and Story can be set for test.

.. code:: python

 import nose

 @nose.allure.feature('Feature1')
 @nose.allure.story('Story1')
 def test_minor():
     assert False

 class TestBar(object):

     @nose.allure.feature('Feature2')
     @nose.allure.story('Story1')
     def test_bar(self):
         pass

To run tests by Feature or Story:

.. code:: bash

 nosetests my_tests/ --with-allure --logdir=tmp --feature="Feature1, Feature2"
 nosetests my_tests/ --with-allure --logdir=tmp --feature="Feature1, Feature2" --story="Story1, Story2"
