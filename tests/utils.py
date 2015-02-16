# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"

import os
from tempfile import mkdtemp
from xml.etree import ElementTree as ET

from nose import run
from nose_allure import Allure


def launch(test_suite, argv=[]):
    tmp_dir = mkdtemp()
    result_dir = os.path.join(tmp_dir, 'results')

    for idx, part in enumerate(test_suite.split('--')):
        file_name = os.path.join(tmp_dir, 'tests_%s.py' % idx)
        with open(file_name, 'wt') as f:
            f.write(part)

    run(defaultTest=tmp_dir, addplugins=[Allure()],
        argv=['', '--with-allure', '--logdir=%s' % result_dir] + argv)

    return [os.path.join(result_dir, name) for name in os.listdir(result_dir)]


def report_for(*args, **kwgs):
    reports = list(filter(
        lambda l: l.endswith('testsuite.xml'), launch(*args, **kwgs)))
    return ET.parse(reports[0])


def environment_for(*args, **kwgs):
    reports = list(filter(
        lambda l: l.endswith('environment.xml'), launch(*args, **kwgs)))
    return ET.parse(reports[0])
