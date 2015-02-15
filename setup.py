# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"


from setuptools import setup

setup(
    name='nose-allure-plugin',
    version='0.1-alpha',
    description='Nose plugin for allure framework',
    author='Sergey Chipiga',
    author_email='chipiga86@gmail.com',
    install_requires=[
        'nose',
        'pytest-allure-adaptor'
    ],
    entry_points={
        'nose.plugins.0.10': [
            'allure = nose_allure:Allure'
        ]
    }
)
