It is a port of `pytest-allure-adaptor <https://github.com/allure-framework/allure-python>`_ for `nose framework <https://github.com/nose-devs/nose>`_.

Usage
=====
.. code:: bash

 nosetests --with-allure --logdir=/path/to/put/results


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

Environment Parameters
----------------------

You can provide test `environment parameters <https://github.com/allure-framework/allure-core/wiki/Environment>`_ such as report name, browser or test server address to allure test report.

.. code:: python

 import nose

 def test_dummy():
     nose.allure.environment(report='Allure report', browser=u'Firefox')

